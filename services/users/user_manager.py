from django.contrib.auth.models import User
from common.utils import dict_to_json
from common.logger import log
from datetime import datetime


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


def user_update(user, body):
    try:
        user.phone_number = body.get('phone_number', user.phone_number)
        date_of_birth_str = body.get('date_of_birth')
        user.date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
        user.gender = body.get('gender', user.gender)
        user.address = body.get('address', user.address)
        user.occupations = body.get('occupations', user.occupations)
        user.account_type = body.get('account_type', user.account_type)
        user.save()
        return dict_to_json(user.as_dict())
    except ValueError:
        log.error('Error while updating data of User %s', user.id)
        return dict_to_json(user.as_dict())


