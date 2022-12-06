from brabbl.utils.models import delete_all_unexpired_sessions_for_user
from django.contrib.auth import logout
from rest_framework.permissions import DjangoObjectPermissions, BasePermission, IsAuthenticatedOrReadOnly

from django.utils.translation import ugettext_lazy as _


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.customer != request.customer:
                delete_all_unexpired_sessions_for_user(user=request.user)
                logout(request)
                return False
            return True


class BrabblDjangoObjectPermission(DjangoObjectPermissions):
    authenticated_users_only = False

    def get_required_permissions(self, method, model_cls):
        method = method.upper()
        return super().get_required_permissions(method, model_cls)

    def get_required_object_permissions(self, method, model_cls):
        method = method.upper()
        return super().get_required_object_permissions(method, model_cls)


class StaffOnlyWritePermission(BrabblDjangoObjectPermission):
    message = _("Object must be created or modified only by an administrator.")

    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view)


class ActivityBasedObjectPermission(BrabblDjangoObjectPermission):
    message = (_("Can't be modified, because other users have already responded on it."))

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) or obj.last_related_activity is None


class OwnershipObjectPermission(BrabblDjangoObjectPermission):
    message = _("Only the creator can modify this object.")

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) or obj.created_by == request.user


class PrivateOnlyIsAuthenticatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.customer and request.customer.is_private:
            if request.user and request.user.is_authenticated and request.user.is_confirmed:
                if request.user.customer != request.customer:
                    delete_all_unexpired_sessions_for_user(user=request.user)
                    logout(request)
                    return False
                return True
        else:
            return True
