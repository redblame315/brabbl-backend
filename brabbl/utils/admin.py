from django.contrib.admin import TabularInline


class SetOfPropertiesInline(TabularInline):
    extra = 0
    template = 'admin/edit_inline/set_of_properties.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj):
        return False
