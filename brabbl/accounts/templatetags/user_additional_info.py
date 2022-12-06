from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.simple_tag
def user_additional_info(user, additional_info, display_fullname):
    """
    Retrub pretty user additional info considering customer settings and user's filled data
    :return: string
    """
    user_info = {}
    result = [""]
    for info in additional_info:
        field = getattr(user, info.key)
        if field:
            if info.key == 'gender':
                user_info[info.key] = user.get_gender_display()
            elif info.key == 'bundesland':
                user_info[info.key] = user.get_bundesland_display()
            else:
                user_info[info.key] = field
    fullname = list_of_fields_to_string(" ", user_info, 'first_name', 'last_name')
    result[0] = fullname if not display_fullname else user.just_username
    info_in_brakes = list_of_fields_to_string(", ", user_info, 'gender', 'year_of_birth')

    if info_in_brakes:
        result[0] += " (" + info_in_brakes + ")"
    job_info = list_of_fields_to_string(", ", user_info, 'organization', 'position')
    if job_info:
        result[0] += ", " + job_info
    address_info = list_of_fields_to_string(", ", user_info, 'postcode', 'city', 'bundesland', 'country')
    if address_info:
        result.append(address_info)
    result.append(user.email + ", " + _("Registration:") + " " + user.date_joined.strftime('%d.%m.%Y'))
    return "\n".join(result)


def list_of_fields_to_string(separator, user_info, *fields):
    """
    Checks is user data exists and concatanate all exist data by separator
    :param separator: result will be separated with thus string
    :param user_info: dict with all data
    :param fields: list of fields
    :return: string
    """
    result = []
    for field in fields:
        if field in user_info:
            result.append(str(user_info[field]))

    return separator.join(result)
