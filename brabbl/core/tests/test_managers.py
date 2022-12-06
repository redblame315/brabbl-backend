from django.test import TestCase

from brabbl.core.tests import factories
from brabbl.core.models import Discussion, Statement, Argument


class HideDeleteTest(TestCase):
    def setUp(self):
        super().setUp()
        self.discussion = factories.ComplexDiscussionFactory.create()
        self.statement = factories.StatementFactory.create(discussion=self.discussion)
        self.argument = factories.ArgumentFactory.create(statement=self.statement)

    def test_hide_discussion(self):
        self.assertEqual(Discussion.objects.visible().count(), 1)
        self.assertEqual(Statement.objects.visible().count(), 1)
        self.assertEqual(Argument.objects.visible().count(), 1)

        self.discussion.delete()

        self.assertEqual(Discussion.objects.visible().count(), 0)
        self.assertEqual(Statement.objects.visible().count(), 0)
        self.assertEqual(Argument.objects.visible().count(), 0)

    def test_hide_statement(self):
        self.assertEqual(Discussion.objects.visible().count(), 1)
        self.assertEqual(Statement.objects.visible().count(), 1)
        self.assertEqual(Argument.objects.visible().count(), 1)

        self.statement.delete()

        self.assertEqual(Discussion.objects.visible().count(), 1)
        self.assertEqual(Statement.objects.visible().count(), 0)
        self.assertEqual(Argument.objects.visible().count(), 0)

    def test_hide_argument(self):
        self.assertEqual(Discussion.objects.visible().count(), 1)
        self.assertEqual(Statement.objects.visible().count(), 1)
        self.assertEqual(Argument.objects.visible().count(), 1)

        self.argument.delete()

        self.assertEqual(Discussion.objects.visible().count(), 1)
        self.assertEqual(Statement.objects.visible().count(), 1)
        self.assertEqual(Argument.objects.visible().count(), 0)
