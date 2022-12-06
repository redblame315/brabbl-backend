import base64
import imghdr
import uuid

from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.request import clone_request

from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _

from brabbl.utils.http import build_absolute_url
from brabbl.utils.models import get_thumbnail_url


class MultipleSerializersViewMixin(object):
    list_serializer_class = None
    update_serializer_class = None

    def get_serializer_class(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        # is it a list view?
        if lookup_url_kwarg not in self.kwargs and self.request.method.lower() != 'post':
            return self.list_serializer_class or self.serializer_class

        # update view?
        if self.request.method.lower() in ['put', 'patch']:
            return self.update_serializer_class or self.serializer_class

        return self.serializer_class

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)  # NOQA

        # use the default serializer for the `response`
        obj = self.get_object()
        return Response(
            self.serializer_class(obj, context=self.get_serializer_context()).data)


class NonNullSerializerMixin(object):
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        for key in list(ret.keys()):
            if ret[key] is None:
                del ret[key]

        return ret


class PermissionSerializerMixin(serializers.Serializer):
    is_deletable = serializers.SerializerMethodField()
    is_editable = serializers.SerializerMethodField()

    def check_user_permission(self, obj, method):
        view = self.context['view']
        request = clone_request(self.context['request'], method)

        if request.user.is_anonymous:
            return False

        success = True

        try:
            view.check_object_permissions(request, obj)
        except APIException as e:
            print("request", request.path)
            success = status.is_success(e.status_code)

        return success

    def get_is_deletable(self, obj):
        return self.check_user_permission(obj, 'delete')

    def get_is_editable(self, obj):
        return self.check_user_permission(obj, 'patch')


class Base64ImageField(serializers.ImageField):
    """
    A django-rest-framework field for handling image-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.

    source: https://github.com/yigitguler/django-rest-framework/commit/c0298042
    """
    ALLOWED_IMAGE_TYPES = ('jpg', 'jpeg', 'png')

    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if isinstance(base64_data, str):
            # Try to decode the file. Return validation error if it fails.
            if 'data:' in base64_data and ';base64,' in base64_data:
                # Break out the header from the base64 content
                header, base64_data = base64_data.split(';base64,')

            try:
                decoded_file = base64.b64decode(base64_data)
            except TypeError:
                raise serializers.ValidationError(_("Picture could not be decoded."))

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            if file_extension not in self.ALLOWED_IMAGE_TYPES:
                raise serializers.ValidationError(
                    _("Please enter a valid image file."))
            complete_file_name = file_name + "." + file_extension
            data = ContentFile(decoded_file, name=complete_file_name)

            return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, filename, decoded_file):
        extension = imghdr.what(filename, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension

    def to_representation(self, image):
        if not image:
            return {}
        small_options = {'size': (64, 64), 'crop': True}
        medium_options = {'size': (290, 200), 'crop': True}
        big_options = {'size': (750, 518), 'crop': True}
        large_options = {'size': (840, 580), 'crop': True}
        return {
            'small': get_thumbnail_url(image, small_options),
            'medium': get_thumbnail_url(image, medium_options),
            'big': get_thumbnail_url(image, big_options),
            'large': get_thumbnail_url(image, large_options),
            'original': build_absolute_url(image.url),
        }
