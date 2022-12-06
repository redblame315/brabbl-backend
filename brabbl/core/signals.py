import os
import signal
from embed_video.backends import YoutubeBackend
from rosetta.signals import post_save as rosetta_post_save

from django.conf import settings
from django.db.models import Avg
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from brabbl.core import models, tasks
from brabbl.utils import logger
from brabbl.utils.rating import denormalize_argument_rating
from brabbl.utils.models import get_thumbnail_url


@receiver(post_save, sender=models.BarometerVote)
def denorm_barometer_values(sender, instance, **kwargs):
    statement = instance.statement
    votes = statement.barometer_votes.all()
    total = votes.count()
    avg = votes.aggregate(Avg('value'))['value__avg']

    statement.barometer_count = total
    statement.barometer_value = avg
    statement.save()


@receiver(pre_save, sender=models.Argument)
def denorm_rating_values_for_argument(sender, instance, **kwargs):
    if instance.status == models.Argument.STATUS_HIDDEN:
        instance.original_rating_of_hidden_argument = instance.rating_value
        instance.original_rating_count_of_hidden_argument = instance.rating_count
        instance.rating_count = 0
        instance.rating_value = 0
    elif not instance.rating_count and not instance.rating_value:
        instance.rating_count = instance.original_rating_count_of_hidden_argument
        instance.rating_value = instance.original_rating_of_hidden_argument


@receiver(post_save, sender=models.Rating)
def denorm_rating_values(sender, instance, **kwargs):
    denormalize_argument_rating(instance.argument)


model_herachie = {
    models.Rating: ['argument'],
    models.Argument: ['reply_to',
                      'statement'],
    models.BarometerVote: ['statement'],
    models.Statement: ['discussion'],
}


@receiver(post_save)
def propagate_last_related_activity(sender, instance, **kwargs):
    try:
        fields = model_herachie[sender]
    except KeyError:
        return

    new_datetime = instance.modified_at

    for field in fields:
        obj = getattr(instance, field)
        if not obj:
            continue

        if not obj.last_related_activity or obj.last_related_activity < new_datetime:
            obj.last_related_activity = new_datetime
            obj.save()
        break


@receiver(post_save, sender=models.Flag)
def flagging_notification(sender, instance, **kwargs):
    if 'created' in kwargs:
        flag = instance
        flag_count = flag.item.flags.count()
        customer = models.Customer.objects.customer_for(flag.item)

        if not customer:  # pragma: no cover
            logger.error('Could not find customer for object %s with id %s',
                         sender.__name__, instance.pk)
            return

        if customer.flag_count_notification <= flag_count:
            customer.send_flag_notification(flag.item)


@receiver(post_save, sender=models.Discussion)
def download_image(sender, instance, **kwargs):
    if not getattr(settings, 'TESTING', False):
        tasks.get_discussion_image(instance)

    if instance.external_id is None or instance.external_id == '-':
        instance.external_id = str(instance.id)
        instance.save()


@receiver(rosetta_post_save)
def reload_for_rosetta(**kwargs):
    pidfile = getattr(settings, 'GUNICORN_PID_FILE', None)
    if pidfile and os.path.exists(pidfile):
        pid = int(open(pidfile).read().strip())
        logger.info('Reloading gunicorn for PO files, PID %s', pid)
        os.kill(pid, signal.SIGHUP)


@receiver(pre_save, sender=models.Statement)
def image_video_xor_add(sender, instance, *args, **kwargs):
    old_data = False
    if instance.pk:
        old_data = models.Statement.objects.get(pk=instance.pk)
    if instance.pk and (instance.video and instance.image.name):
        if bool(old_data.image.name):
            instance.image = None
        elif old_data.video:
            instance.video = None

    if instance.video:
        instance.thumbnail = YoutubeBackend(instance.video).thumbnail
    elif instance.thumbnail and not bool(instance.image.name):
        instance.thumbnail = ''
    elif instance.image and not old_data or (old_data and (
            not bool(old_data.image.name) or instance.image.size != old_data.image.size)):
        instance.thumbnail = ''


@receiver(post_save, sender=models.Statement)
def image_thumbnail(sender, instance, **kwargs):
    if instance.image and instance.thumbnail == '':
        instance.thumbnail = get_thumbnail_url(instance.image, {'size': (300, 206), 'crop': True})
        instance.save()
