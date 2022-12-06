from rest_framework.authtoken.models import Token

from brabbl.accounts.tests.factories import CustomerFactory, UserFactory
from brabbl.core.tests import factories as brabbl_factories


class BrabblFactory(object):
    USER_USERNAME = 'hans.lustig'
    USER_PASSWORD = 'test_password'
    SIMPLE_DISCUSSION_ID = 'a30fc8b06'
    COMPLEX_DISCUSSION_ID = 'b30fc8b06'

    def _get(self, factory, amount=1, **arguments):
        model = factory._meta.model
        qs = model.objects.filter(**arguments)
        if qs.exists():
            if qs.count() == 1:
                return qs.all()[0]
            return list(qs.all())

        if amount == 1:
            return factory.create(**arguments)
        return factory.create_batch(amount, **arguments)

    def clear(self):
        for factory in [UserFactory,
                        brabbl_factories.TagFactory,
                        brabbl_factories.WordingFactory,
                        brabbl_factories.BaseDiscussionFactory,
                        brabbl_factories.StatementFactory]:
            factory._meta.model.objects.all().delete()

    @property
    def customer(self):
        return self._get(CustomerFactory)

    @property
    def user(self):
        user = self._get(UserFactory, customer=self.customer, username=self.USER_USERNAME)
        user.set_password(self.USER_PASSWORD)
        user.save()
        return user

    @property
    def user_token(self):
        user_token, _ = Token.objects.get_or_create(user=self.user)
        return user_token.key

    @property
    def wording(self):
        return self._get(brabbl_factories.WordingFactory)

    @property
    def tags(self):
        return self._get(brabbl_factories.TagFactory, amount=3,
                         customer=self.customer)

    @property
    def simple_discussion(self):
        discussion = self._get(
            brabbl_factories.SimpleDiscussionFactory,
            customer=self.customer,
            external_id=self.SIMPLE_DISCUSSION_ID,
            created_by=self.user,
            discussion_wording=self.wording,
        )

        argument = self._get(
            brabbl_factories.ArgumentFactory,
            statement=discussion.statements.all()[0],
            created_by=self.user,
            reply_to=None
        )

        self._get(
            brabbl_factories.ArgumentFactory,
            statement=discussion.statements.all()[0],
            created_by=self.user,
            reply_to=argument
        )

        return discussion

    @property
    def complex_discussion(self):
        discussion = self._get(
            brabbl_factories.ComplexDiscussionFactory,
            customer=self.customer,
            external_id=self.COMPLEX_DISCUSSION_ID,
            created_by=self.user,
            discussion_wording=self.wording,
            multiple_statements_allowed=True,
            user_can_add_replies=True,
        )
        self._get(
            brabbl_factories.StatementFactory,
            discussion=discussion,
            statement='First Statement',
            created_by=self.user,
        )
        return discussion

    @classmethod
    def populate_database(cls):
        factory = BrabblFactory()

        # generate auth objects
        factory.customer
        factory.user

        # global objects
        factory.wording
        factory.tags  # generates 3 Tags

        # create a discussion
        factory.simple_discussion
        factory.complex_discussion
