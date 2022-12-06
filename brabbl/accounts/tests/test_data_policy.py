from pytest import mark, fixture

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from django.utils.timezone import localtime, now

from brabbl.accounts.models import Customer, DataPolicyAgreement

from . import factories


@fixture
def data_policy_fixture():
    policy = factories.DataPolicyFactory(
        title='Test-Title',
        text='Test-Text',
        version_number=1.0
    )
    customer = factories.CustomerFactory.create(
        displayed_username=Customer.DISPLAY_USERNAME,
        data_policy_version=policy
    )
    user = factories.UserFactory.create(customer=customer)
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION='Token ' + Token.objects.get_or_create(user=user)[0].key,
    )
    return policy, user, customer, client


@mark.django_db
def test_data_policy_agreed(data_policy_fixture):
    policy, user, customer, client = data_policy_fixture
    DataPolicyAgreement.objects.create(
        user=user,
        data_policy=policy,
        ip_address='192.0.0.1',
        date_accepted=localtime(now())
    )
    assert user.has_accepted_current_data_policy()
    # check if the API correctly returns the data policy flag
    response = client.get('/api/v1/account/', HTTP_X_BRABBL_TOKEN=customer.embed_token)
    assert response.data['has_accepted_current_data_policy'] is True


@mark.django_db
def test_data_policy_outdated(data_policy_fixture):
    policy, user, customer, client = data_policy_fixture
    updated_policy = factories.DataPolicyFactory(
        title='Test-Title-2',
        text='Test-Text-2',
        version_number=2.0
    )
    customer.data_policy_version = updated_policy
    customer.save()
    DataPolicyAgreement.objects.create(
        user=user,
        data_policy=policy,
        ip_address='192.0.0.1',
        date_accepted=localtime(now())
    )
    assert user.has_accepted_current_data_policy() is False
    # check if also the API correctly returns the correct data policy flag
    response = client.get('/api/v1/account/', HTTP_X_BRABBL_TOKEN=customer.embed_token)
    assert response.data['has_accepted_current_data_policy'] is False
    # accept latest data policy
    response = client.post(
        '/api/v1/account/confirm-data-policy/', HTTP_X_BRABBL_TOKEN=customer.embed_token)
    # check again, user should now be up to date
    assert user.has_accepted_current_data_policy() is True
