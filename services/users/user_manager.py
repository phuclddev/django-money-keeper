from django.contrib.auth.models import User
from common.utils import dict_to_json
from django.utils import timezone


def get_infos_json(user_name):
    """
    From Username then Return User info as Json
    """
    if not user_name:
        return {}
    user = User.objects.get(username=user_name)
    user = user.__dict__
    user.pop('_state', None)
    user.pop('password', None)
    user.pop('is_superuser', None)
    user_json = dict_to_json(user)
    return user_json


