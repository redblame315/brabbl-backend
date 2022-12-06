from django.conf import settings


def global_variables(request):
    return {
        'THEME_LOCATION_URL': settings.THEME_LOCATION_URL,
    }
