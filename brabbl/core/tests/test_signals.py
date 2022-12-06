from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.test import TestCase

from brabbl.core.models import Argument, BarometerVote, Rating, Statement
from brabbl.core.tests import factories
from brabbl.utils import math
from brabbl.utils.models import LastActivityMixin
from ..models import Flag


class StatementSignalTests(TestCase):
    def test_denorm_values(self):
        discussion = factories.SimpleDiscussionFactory.create()
        statement = discussion.statements.all()[0]

        self.assertEqual(statement.barometer_count, 0)
        self.assertEqual(statement.barometer_value, 0)
        mean = 0

        for i in range(10):
            # generate alternating rating values between [-3;3]
            rating = (i % 4) * (-1) ** i
            mean = math.iterative_mean(mean, i, rating)

            BarometerVote.objects.create(
                statement=statement,
                user=factories.UserFactory.create(),
                value=rating,
            )

            statement = Statement.objects.get(id=statement.id)
            self.assertEqual(statement.barometer_count, i + 1)
            self.assertAlmostEqual(float(statement.barometer_value), mean, places=1)


class ArgumentSignalTest(TestCase):
    def test_denorm_values(self):
        discussion = factories.SimpleDiscussionFactory.create()
        statement = discussion.statements.all()[0]
        argument = factories.ArgumentFactory.create(
            statement=statement,
            created_by=statement.created_by,
        )
        self.assertEqual(statement.barometer_count, 0)
        self.assertEqual(statement.barometer_value, 0)
        mean = 0

        for i in range(10):
            rating = i % 6
            mean = math.iterative_mean(mean, i, rating)

            Rating.objects.create(
                argument=argument,
                user=factories.UserFactory.create(),
                value=rating,
            )

            argument = Argument.objects.get(pk=argument.pk)
            self.assertEqual(argument.rating_count, i + 1)
            self.assertAlmostEqual(float(argument.rating_value), mean, places=1)

        argument.status = Argument.STATUS_HIDDEN
        argument.save()
        argument = Argument.objects.get(pk=argument.pk)
        self.assertEqual(argument.rating_count, 0)
        self.assertEqual(argument.rating_value, 0)


def paired_iter(it):
    token = next(it)
    for lookahead in it:
        yield (token, lookahead)
        token = lookahead
    yield (token, None)


class LastActivityTest(TestCase):
    def test_last_activity_simple_discussion(self):
        discussion = factories.SimpleDiscussionFactory()
        statement = discussion.statements.all()[0]
        self.assertEqual(discussion.last_related_activity, statement.modified_at)

    def assertLastActivity(self, objs):
        for obj, peek in paired_iter(iter(objs)):
            if not isinstance(obj, LastActivityMixin):  # Vote/Rating
                continue

            if peek is None:
                self.assertEqual(obj.last_related_activity, None)
            else:
                self.assertEqual(obj.last_related_activity, peek.modified_at)

    def test_last_activity_propagation(self):
        discussion = factories.ComplexDiscussionFactory()
        self.assertLastActivity([discussion])

        statement = factories.StatementFactory(discussion=discussion)
        self.assertLastActivity([discussion, statement])

        argument = factories.ArgumentFactory(statement=statement)
        self.assertLastActivity([discussion, statement, argument])

        reply = factories.ArgumentFactory(statement=statement,
                                          reply_to=argument)
        self.assertLastActivity([discussion, statement, argument, reply])

    def test_vote_propagation(self):
        discussion = factories.ComplexDiscussionFactory()
        statement = factories.StatementFactory(discussion=discussion)
        argument = factories.ArgumentFactory(statement=statement)

        vote = BarometerVote.objects.create(statement=statement,
                                            user=argument.created_by,
                                            value=1)
        self.assertLastActivity([discussion, statement, vote])

    def test_rating_propagation(self):
        discussion = factories.ComplexDiscussionFactory()
        statement = factories.StatementFactory(discussion=discussion)
        argument = factories.ArgumentFactory(statement=statement)
        factories.ArgumentFactory(statement=statement, reply_to=argument)

        # test rate
        vote = Rating.objects.create(argument=argument,
                                     user=argument.created_by,
                                     value=1)
        self.assertLastActivity([discussion, statement, argument, vote])


class FlagSignalTests(TestCase):
    def setUp(self):
        super().setUp()
        self.customer = factories.CustomerFactory.create()
        self.discussion = factories.SimpleDiscussionFactory(customer=self.customer)
        self.statement = self.discussion.statements.all()[0]
        self.argument = factories.ArgumentFactory.create(
            statement=self.statement,
            created_by=self.statement.created_by,
        )

    def flag_object(self, obj):
        return Flag.objects.create(
            content_type=ContentType.objects.get_for_model(obj.__class__),
            object_id=obj.id,
            user=factories.UserFactory.create())

    def _test_flag_object(self, obj):
        for i in range(1, self.customer.flag_count_notification):
            self.flag_object(obj)
            self.assertEqual(len(mail.outbox), 0)

        self.flag_object(obj)
        self.assertEqual(len(mail.outbox), 1)

        body = mail.outbox[0].body
        self.assertEqual('support@brabbl.com', mail.outbox[0].from_email)
        self.assertTrue(self.customer.moderator_email in mail.outbox[0].recipients())
        self.assertTrue(obj.__class__.__name__ in body)
        self.assertTrue(str(obj.id) in body)
        self.assertTrue(self.discussion.source_url in body)

    def test_flag_argument(self):
        self._test_flag_object(self.argument)

    def test_flag_argument_1(self):
        # test lower limit
        self.customer.flag_count_notification = 1
        self.customer.save()
        self._test_flag_object(self.argument)

    def test_flag_statement(self):
        self._test_flag_object(self.statement)

    def test_flag_statement_1(self):
        # test lower limit
        self.customer.flag_count_notification = 1
        self.customer.save()
        self._test_flag_object(self.statement)
