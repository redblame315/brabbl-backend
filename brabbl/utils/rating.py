from django.db.models import Avg


def denormalize_argument_rating(argument):
    """
    Denormalize argument rating.

    Set to zero hidden argument's rating.
    """
    if argument.status == argument.STATUS_ACTIVE:
        total = argument.ratings.all().count()
        avg = argument.ratings.all().aggregate(Avg('value'))['value__avg']
    else:
        total = 0
        avg = 0
    argument.rating_count = total
    argument.rating_value = avg
    argument.save()
