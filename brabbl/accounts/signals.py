from django.db.models.signals import post_save
from django.dispatch import receiver
from brabbl.accounts import models


@receiver(post_save, sender=models.Customer)
def update_embed_token_in_username(sender, instance, **kwargs):
    """
    If embed token was changed update it for every user of this customer
    """
    for user in instance.user_set.all():
        try:
            username, customer_token = user.username.split("+")
            user.username = "{}+{}".format(username, instance.embed_token)
            user.save()
        except ValueError:
            pass
