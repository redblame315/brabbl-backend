import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, DjangoClient

from brabbl.accounts.tests.factories import CustomerFactory, PrivateCustomerFactory, UserFactory


class BrabblClient(APIRequestFactory, DjangoClient):
    def as_customer(self, customer):
        self._customer = customer

    def as_user(self, user):
        self._user = user

    def set_referer(self, referer):
        self._referer = referer

    def request(self, **kwargs):
        # Ensure that every required HEADER get added to every request.
        if hasattr(self, '_customer') and self._customer:
            kwargs.update({
                'HTTP_X_BRABBL_TOKEN': self._customer.embed_token,
            })

        if hasattr(self, '_user') and self._user:
            token, created = Token.objects.get_or_create(user=self._user)
            kwargs.update({
                'HTTP_AUTHORIZATION': 'Token {0}'.format(token.key)
            })

        if hasattr(self, '_referer') and self._referer:
            kwargs.update({
                'HTTP_REFERER': self._referer
            })

        return super(BrabblClient, self).request(**kwargs)


class BrabblAPITestCase(APITestCase):
    client_class = BrabblClient
    user_password = 'TEST_PASSWORD'

    def setUp(self):
        self.customer = CustomerFactory.create()
        self.user = UserFactory.create(customer=self.customer)
        self.user.set_password(self.user_password)
        self.user.save()

    def get_object(self):  # pragma: no cover
        raise NotImplemented()


class PrivateBrabblAPITestCase(APITestCase):
    client_class = BrabblClient
    user_password = 'TEST_PASSWORD'

    def setUp(self):
        self.customer = PrivateCustomerFactory.create()
        self.user = UserFactory.create(customer=self.customer, is_confirmed=True)
        self.user.set_password(self.user_password)
        self.user.save()

    def get_object(self):  # pragma: no cover
        raise NotImplemented()


class CreateTestMixin(object):
    create_customer_required = True
    create_user_required = True
    create_status_code = status.HTTP_201_CREATED
    create_required_fields = []

    def get_create_url(self):
        return reverse('v1:{0}-list'.format(self.base_name))

    def get_create_data(self):  # pragma: no cover
        raise NotImplemented()

    def test_customer_required_for_create(self):
        self.client._customer = None
        response = self.client.post(self.get_create_url(), data=self.get_create_data())

        if self.create_customer_required:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        else:
            self.assertEqual(response.status_code, self.create_status_code)

    def test_user_required_for_create(self):
        if self.create_customer_required:
            self.client.as_customer(self.customer)

        self.client._user = None
        response = self.client.post(self.get_create_url(), data=self.get_create_data(),
                                    format='json')

        if self.create_user_required:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        else:
            self.assertEqual(response.status_code, self.create_status_code)

    def set_create_headers(self, as_user=None):
        if self.create_customer_required:
            self.client.as_customer(self.customer)
        if self.create_user_required:
            self.client.as_user(as_user or self.user)

    def create(self, data=None, status_code=None, as_user=None):
        self.set_create_headers(as_user=as_user)
        status_code = status_code or self.create_status_code
        if data is None:
            data = self.get_create_data()

        response = self.client.post(self.get_create_url(), data=data, format="json")
        self.assertEqual(response.status_code, status_code)
        return response

    def test_required_fields(self):
        self.set_create_headers()
        if not self.create_required_fields:
            return

        response = self.create(data={}, status_code=status.HTTP_400_BAD_REQUEST)
        for fieldname in self.create_required_fields:
            self.assertTrue(
                fieldname in response.data.keys(),
                '{0} should be required'.format(fieldname))

    def test_create(self):
        return self.create(data=self.get_create_data())


class RetrieveTestMixin(object):
    retrieve_customer_required = True
    retrieve_user_required = False

    lookup_param = 'pk'

    def get_retrieve_url(self, obj=None):
        if obj is None:
            obj = self.get_object()
        obj_id = getattr(obj, self.lookup_param)
        if self.base_name == 'discussion':
            return '/api/v1/discussions/detail/?external_id=%s' % obj_id
        elif self.base_name == 'discussion_list':
            return '/api/v1/discussion_list/detail/?url=%s' % obj_id
        return reverse('v1:{0}-detail'.format(self.base_name), args=(obj_id,))

    def test_customer_required_for_retrieve(self):
        self.client._customer = None
        response = self.client.get(self.get_retrieve_url())

        if self.retrieve_customer_required:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_required_for_retrieve(self):
        if self.retrieve_customer_required:
            self.client.as_customer(self.customer)

        self.client._user = None
        response = self.client.get(self.get_retrieve_url())

        if self.retrieve_user_required:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def set_retrieve_headers(self):
        if self.retrieve_customer_required:
            self.client.as_customer(self.customer)
        if self.retrieve_user_required:
            self.client.as_user(self.user)

    def retrieve(self, obj=None, status_code=status.HTTP_200_OK):
        self.set_retrieve_headers()
        response = self.client.get(self.get_retrieve_url(obj=obj))
        self.assertEqual(response.status_code, status_code)
        return response

    def test_retrieve(self):
        return self.retrieve()


class UpdateTestMixin(object):
    update_customer_required = True
    update_user_required = True

    lookup_param = 'pk'

    def get_update_url(self, obj=None):
        if obj is None:
            obj = self.get_object()
        obj_id = getattr(obj, self.lookup_param)
        if self.base_name == 'discussion':
            return '/api/v1/discussions/detail/?external_id=%s' % obj_id
        elif self.base_name == 'discussion_list':
            return '/api/v1/discussion_list/detail/?url=%s' % obj_id
        return reverse('v1:{0}-detail'.format(self.base_name), args=(obj_id,))

    def get_update_data(self):
        raise NotImplemented()

    def test_customer_required_for_update(self):
        self.client._customer = None
        response = self.client.put(self.get_update_url(), format='json')

        if self.update_customer_required:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_required_for_update(self):
        if self.retrieve_customer_required:
            self.client.as_customer(self.customer)

        self.client._user = None
        response = self.client.put(self.get_update_url(), format='json')

        if self.update_user_required:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def set_update_headers(self, as_user=None):
        if self.update_customer_required:
            self.client.as_customer(self.customer)
        if self.update_user_required:
            self.client.as_user(as_user or self.user)

    def update(self, data=None, status_code=status.HTTP_200_OK, as_user=None):
        self.set_update_headers(as_user=as_user)
        if data is None:
            data = self.get_update_data()
        response = self.client.patch(self.get_update_url(), data=json.dumps(data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        return response

    def test_update(self):
        data = self.get_update_data()
        response = self.update(data)
        for field, value in data.items():
            self.assertEqual(response.data[field], value)
        return response


class DestroyTestMixin(object):
    destroy_customer_required = True
    destroy_user_required = True

    lookup_param = 'pk'

    def get_destroy_url(self, obj=None):
        if obj is None:
            obj = self.get_object()
        obj_id = getattr(obj, self.lookup_param)
        if self.base_name == 'discussion':
            return '/api/v1/discussions/detail/?external_id=%s' % obj_id
        elif self.base_name == 'discussion_list':
            return '/api/v1/discussion_list/detail/?url=%s' % obj_id
        return reverse('v1:{0}-detail'.format(self.base_name), args=(obj_id,))

    def test_customer_required_for_destroy(self):
        self.client._customer = None
        response = self.client.delete(self.get_destroy_url())

        if self.destroy_customer_required:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        else:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_required_for_destroy(self):
        if self.retrieve_customer_required:
            self.client.as_customer(self.customer)

        self.client._user = None
        response = self.client.delete(self.get_update_url())

        if self.destroy_user_required:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        else:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def set_destroy_headers(self, as_user=None):
        if self.destroy_customer_required:
            self.client.as_customer(self.customer)
        if self.destroy_user_required:
            self.client.as_user(as_user or self.user)

    def destroy(self, data=None, status_code=status.HTTP_204_NO_CONTENT, as_user=None):
        self.set_destroy_headers(as_user=as_user)
        response = self.client.delete(self.get_destroy_url())
        self.assertEqual(response.status_code, status_code)
        return response

    def test_destroy(self):
        return self.destroy()


class ListTestMixin(object):
    list_customer_required = True
    list_user_required = False

    def get_list_url(self):
        return reverse('v1:{0}-list'.format(self.base_name))

    def test_customer_required_for_list(self):
        response = self.client.get(self.get_list_url())

        if self.list_customer_required:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_required_for_list(self):
        if self.list_customer_required:
            self.client.as_customer(self.customer)
        response = self.client.get(self.get_list_url())

        if self.list_user_required:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def set_list_headers(self):
        if self.list_customer_required:
            self.client.as_customer(self.customer)
        if self.list_user_required:
            self.client.as_user(self.user)

    def get_list(self, status_code=status.HTTP_200_OK):
        self.set_list_headers()

        response = self.client.get(self.get_list_url())
        self.assertEqual(response.status_code, status_code)
        # result should be a list
        self.assertTrue(isinstance(response.data, list))

        return response

    def test_list(self):
        self.get_object()  # generate an object
        response = self.get_list()
        self.assertEqual(len(response.data), 1)
        return response


class ViewSetTestMixin(CreateTestMixin,
                       RetrieveTestMixin,
                       UpdateTestMixin,
                       DestroyTestMixin,
                       ListTestMixin):
    pass
