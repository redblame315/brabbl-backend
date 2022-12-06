import factory

from brabbl.accounts.tests.factories import CustomerFactory, UserFactory
from .. import models


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Tag %d' % n)

    class Meta:
        model = models.Tag


class WordingValueFactory(factory.django.DjangoModelFactory):
    wording = factory.SubFactory('brabbl.core.tests.factories.WordingFactory')
    name = factory.Sequence(lambda n: 'Wording %d' % n)
    value = factory.Sequence(lambda n: n)

    class Meta:
        model = models.WordingValue


class WordingFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Wording %d' % n)
    description = factory.Sequence(lambda n: 'Wording Description %d' % n)

    class Meta:
        model = models.Wording

    @factory.post_generation
    def words(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        # generate WordingValues
        for value, _ in models.WordingValue.CHOICES:
            WordingValueFactory.create(wording=self, value=value)


class ArgumentFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    is_pro = factory.Sequence(lambda n: bool(n % 2))
    title = factory.Sequence(lambda n: 'Argument %d' % n)
    text = factory.Sequence(lambda n: 'ArgumentText %d' % n)

    class Meta:
        model = models.Argument


class StatementFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    statement = factory.Sequence(lambda n: 'Statement %d' % n)

    class Meta:
        model = models.Statement

    @factory.post_generation
    def arguments(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        # generate WordingValues
        if extracted:
            for argument in extracted:
                self.arguments.add(argument)
        else:
            try:
                argument = ArgumentFactory._meta.model.objects.all()[0]
            except IndexError:
                pass
            else:
                self.arguments.add(argument)


class DiscussionListFactory(factory.django.DjangoModelFactory):
    url = factory.Sequence(lambda n: 'http://example.com/%d/' % n)
    search_by = models.DiscussionList.SEARCH_BY_ALL_TAGS

    class Meta:
        model = models.DiscussionList


class BaseDiscussionFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(CustomerFactory)
    created_by = factory.SubFactory(UserFactory)

    external_id = factory.Sequence(lambda n: 'externalid%d' % n)
    source_url = factory.Sequence(lambda n: 'http://example.com/%d/' % n)
    statement = factory.Sequence(lambda n: 'Statement %d' % n)
    discussion_wording = factory.SubFactory(WordingFactory)

    class Meta:
        model = models.Discussion

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        # generate WordingValues
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            try:
                tag = TagFactory._meta.model.objects.all()[0]
            except IndexError:
                tag = TagFactory.create(customer=self.customer)
            self.tags.add(tag)


class SimpleDiscussionFactory(BaseDiscussionFactory):
    class Meta:
        model = models.Discussion

    @factory.post_generation
    def statements(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        StatementFactory.create(
            discussion=self,
            created_by=self.created_by,
        )


class NotificationWordingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NotificationWording


class NotificationWordingMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NotificationWordingMessage


class MarkdownWordingMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MarkdownWordingMessage


class ComplexDiscussionFactory(BaseDiscussionFactory):
    multiple_statements_allowed = True
    user_can_add_replies = True

    class Meta:
        model = models.Discussion


class PrivateDiscussionFactory(BaseDiscussionFactory):
    is_private = True

    class Meta:
        model = models.Discussion
