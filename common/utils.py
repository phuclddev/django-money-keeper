from django import http
from .constants import *
import json
from datetime import date as date_type, time as time_type
from django.db.models.fields.files import FieldFile
import requests
import traceback
from django.urls import reverse
from common.logger import log
from django.conf import settings
from decimal import Decimal
from django.db.models.fields.files import ImageFieldFile


# def dict_to_json(data, fields=None, exclude=None, **kwargs):
#     """
#     Return a JSON-dumpable dict
#     """
#     for attr in data:
#         print(data[attr])
#         if isinstance(data[attr], time_type):
#             data[attr] = data[attr].strftime(kwargs.get('time_format', '%H:%M:%S'))
#         elif isinstance(data[attr], date_type):
#             data[attr] = data[attr].strftime(kwargs.get('date_format', '%Y-%m-%d %H:%M:%S'))
#         elif isinstance(data[attr], FieldFile):
#             file_data = {}
#             for k in kwargs.get('file_attributes', ('url',)):
#                 file_data[k] = data[attr].__getattribute__(k) if hasattr(data[attr], k) else ''
#             data[attr] = file_data
#         elif isinstance(data[attr], Decimal):
#             data[attr] = float(data[attr])
#         elif isinstance(data[attr], ImageFieldFile):
#             file_data = {}
#             for k in kwargs.get('file_attributes', ('url',)):
#                 print(file_data[k])
#                 file_data[k] = data[attr].__getattribute__(k) if hasattr(data[attr], k) else ''
#             data[attr] = file_data
#     return data

def dict_to_json(data):
    """
        Return a clean dict
    """
    for key, value in data.items():
        if isinstance(value, time_type):
            data[key] = value.strftime('%H:%M:%S')
        elif isinstance(value, date_type):
            data[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, Decimal):
            data[key] = float(value)
        elif isinstance(value, ImageFieldFile):
            data[key] = str(value)
    # json_data = json.dumps(data)
    json_data = data
    return json_data


def to_json(data, ensure_ascii=False, ensure_bytes=False, default=None):
    """
    Use in api_response_data
    Return data in Json
    """
    result = json.dumps(data, ensure_ascii=ensure_ascii, separators=(',', ':'), default=default)
    if ensure_bytes and isinstance(result, str):
        result = result.encode('utf-8')
    return result


def api_response_data(data, status=FAIL):
    """
    Use in api app to return response
    """
    if status == SUCCESSFUL:
        data = {
            'status': SUCCESSFUL,
            'payload': data
        }
    else:
        data['status'] = FAIL
    return http.HttpResponse(to_json(data), content_type='application/json; charset=utf-8')


def objects_to_json(objects):
    """
    Converts a Django QuerySet to a JSON string
    """
    objects_list = []
    for object in objects:
        object_json = object.as_json()
        objects_list.append(object_json)
    return objects_list

# Utils for Google login
def _get_user_info(code):
    ret_val = {}
    if code is None:
        log.error('No code, redirect to Login url')
        return ret_val

    GOOGLE = settings.GOOGLE
    data = {
        'code': code,
        'client_id': GOOGLE['CLIENT_ID'],
        'client_secret': GOOGLE['CLIENT_SECRET'],
        'redirect_uri': _login_url(),
        'grant_type': 'authorization_code'
    }
    get_token_url = 'https://www.googleapis.com/oauth2/v4/token'
    token_in_dict = {}
    try:
        r = requests.post(
            get_token_url,
            data=data,
            verify=False
        )
        token_in_dict = r.json()
    except Exception as e:
        log.error('Cannot get token from code. Exception: %s', str(e))
        return ret_val

    id_token = token_in_dict.get('id_token', None)
    if id_token is None:
        log.error('Cannot get token from code: %s, %s', code, token_in_dict)
        return ret_val

    # Else:
    get_user_info_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s' % (
        id_token
    )
    try:
        r = requests.get(get_user_info_url, verify=False)
        ret_val = r.json()
    except Exception as e:
        log.error(
            'Cannot get user info from token: %s. Exception: %s, %s',
            id_token,
            str(e),
            traceback.format_exc()
        )
        return ret_val

    return ret_val


def _login_url():
    login_callback_path = reverse('login-callback')
    return remove_double_slashes(settings.HOME_PAGE + '/' + login_callback_path)


def remove_double_slashes(url):
    ret_val = ''
    parts = url.split('://')
    return '://'.join([part.replace('//', '/') for part in parts])


def _home():
    return remove_double_slashes(settings.HOME_PAGE + '/')
# End Utils for Google login





