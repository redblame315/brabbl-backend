from django.test import TestCase
from django.conf import settings
from . import factories
from .. import models
from brabbl.utils.string import add_widget_hashtag


class LastActivityTest(TestCase):
    def assertLastActivity(self, obj):
        self.assertEqual(obj.last_related_activity, None)
        self.assertEqual(obj.last_activity, obj.modified_at)

    def test_initial_last_activity(self):
        discussion = factories.ComplexDiscussionFactory.create()
        self.assertLastActivity(discussion)
        statement = factories.StatementFactory.create(discussion=discussion)
        self.assertLastActivity(statement)
        argument = factories.ArgumentFactory.create(statement=statement)
        self.assertLastActivity(argument)


class DiscussionTest(TestCase):
    def test_download_image(self):
        discussion = factories.SimpleDiscussionFactory(
            image_url='',
            source_url='https://ogp.me/',
        )
        self.assertEqual(discussion.image_url, '')

        with self.settings(TESTING=False):
            discussion.save()  # trigger signal and task

        discussion = models.Discussion.objects.get(pk=discussion.pk)
        self.assertEqual(discussion.image_url, 'https://ogp.me/logo.png')

    def test_hash_striping(self):
        discussion = factories.SimpleDiscussionFactory()
        discussion.source_url = add_widget_hashtag(discussion.source_url)
        discussion.save()
        self.assertNotIn(settings.WIDGET_HASHTAG, discussion.source_url)


class NotificationWordingModel(TestCase):
    def test_save(self):
        wording = factories.NotificationWordingFactory.create()
        self.assertEqual(wording.model_properties.count(),
                         len(models.NotificationWordingMessage.FIELD_LIST))
