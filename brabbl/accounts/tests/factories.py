import factory

from django.contrib.auth.models import Permission, Group

from .. import models


class CustomerFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Customer %d' % n)
    moderator_email = factory.Sequence(lambda n: 'mod-%d@example.com' % n)
    allowed_domains = factory.Sequence(lambda n: 'example-%d.com' % n)
    invitations_pending = factory.Sequence(lambda n: ('invite-%d@example.com\n'
                                                      'hans.lustig@example.com') % n)

    class Meta:
        model = models.Customer


class PrivateCustomerFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Private Customer %d' % n)
    moderator_email = factory.Sequence(lambda n: 'mod-%d@example.com' % n)
    allowed_domains = factory.Sequence(lambda n: 'example-%d.com' % n)
    invitations_pending = factory.Sequence(lambda n: ('invite-%d@example.com\n'
                                                      'hans.lustig@example.com\nhans.lustig@example.com2') % n)

    is_private = True

    class Meta:
        model = models.Customer


class UserFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(CustomerFactory)
    email = factory.Sequence(lambda n: 'user-%d@example.com' % n)
    username = factory.Sequence(lambda n: 'Username %d' % n)
    first_name = factory.Sequence(lambda n: 'FirstName%d' % n)
    last_name = factory.Sequence(lambda n: 'LastName%d' % n)
    is_active = True

    class Meta:
        model = models.User


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group


def add_staff_permissions_to_user(user):
    """
    Get all permissions to user
    :param user: UserObject
    """
    user.user_permissions.add(*Permission.objects.all())
    user.save()


class DataPolicyFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.DataPolicy


class StaffFactory(factory.django.DjangoModelFactory):
    is_staff = True

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        if create:
            add_staff_permissions_to_user(obj)

    class Meta:
        model = models.User


class EmailGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EmailGroup


class EmailTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EmailTemplate
