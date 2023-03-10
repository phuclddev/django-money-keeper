from services.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from common.utils import api_response_data
from common import constants
from common.constants import *
from services.users import user_manager
from django.views.decorators.csrf import csrf_exempt
from .schema import *
from common.decorator import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from common.logger import log
from django.contrib.auth import authenticate as django_authenticate, login as django_login, logout as django_logout
from urllib import parse
from django.shortcuts import redirect
from common.utils import _get_user_info, _home, _login_url
from common.utils import dict_to_json
import re
import datetime


DEFAULT_PASSWORD = '1'
# Google Login -----------------------------------------------------------------
@log_request()
def login(request):
    GOOGLE = settings.GOOGLE
    login_url = '%s?client_id=%s&redirect_uri=%s&response_type=code&scope=%s&access_type=offline&include_granted_scopes=true&state=state_parameter_passthrough_value' % (
        GOOGLE['BASE_URL'],
        GOOGLE['CLIENT_ID'],
        parse.quote(_login_url(), safe=''),
        parse.quote(GOOGLE['SCOPE'], safe='')
    )
    # return
    return redirect(login_url)


@log_request()
@sync_to_async()
def logout(request):
    django_logout(request)
    return redirect(_home())


@log_request()
@sync_to_async()
def google_oauth2_callback(request):
    code = request.GET.get('code', None)
    user_info_in_dict = _get_user_info(code)
    log.info('Received user info from Google %s, code: %s', user_info_in_dict, code)
    if user_info_in_dict.get('email', None) is None:
        log.error('Cannot get user info from token. Received data from Google %s', user_info_in_dict)
        return redirect(_home())

    email = user_info_in_dict.get('email', None)
    try:
        user = User.objects.get(username=email)
        user.nickname = user_info_in_dict.get('name', '')
        user.first_name = user_info_in_dict.get('given_name', '')
        user.last_name = user_info_in_dict.get('family_name', '')
        user.avatar = user_info_in_dict.get('picture', '')
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=DEFAULT_PASSWORD,
            first_name=user_info_in_dict.get('given_name', ''),
            last_name=user_info_in_dict.get('family_name', ''),
            avatar=user_info_in_dict.get("picture", "")
        )
        user.is_staff = False
        user.is_superuser = False
        user.save()

    user = django_authenticate(username=user.username, password=DEFAULT_PASSWORD)
    print(user.username)
    django_login(request, user)
    log.info('Login successfully. User Id: %s', user.id)
    return redirect(_home())


@csrf_exempt
@my_login_required
@require_http_methods(["GET", "PUT"])
@parse_params(user_update_schema, ['PUT'])
def detail(request, body):
    user = request.user
    if request.method == 'GET':
        log.info('Get user info successfully. User Id: %s', user.id)
        return api_response_data({
            "user": dict_to_json(user.as_dict()),
        }, SUCCESSFUL)
    elif request.method == 'PUT':
        phone_number = body.get('phone_number')
        if phone_number is not None and not re.match(r'^\d{10}$', phone_number):
            return api_response_data({
            "error": constants.ErrorCode.ERROR_PHONE_NUMBER,
        })
        date_of_birth = body.get('date_of_birth')
        birth_date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        if date_of_birth is not None and birth_date > datetime.date.today():
            return api_response_data({
            "error": constants.ErrorCode.ERROR_DATE_OF_BIRTH,
        })
        user_update = user_manager.user_update(user, body)
        log.info('Update user info successfully. User Id: %s', user.id)
        return api_response_data({
            "user": user_update,
        }, SUCCESSFUL)




#
# # Content-Type: application/x-www-form-urlencoded
# @csrf_exempt
# @require_http_methods(["POST"])
# def my_login(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         user_name = user.get_username()
#         user_infos = user_manager.get_infos_json(user_name)
#         return api_response_data({
#         "user": user_infos,
#     }, SUCCESSFUL)
#     else:
#         return api_response_data({
#         "error": constants.ErrorCode.ERROR_INVALID_CREDENTIALS,
#     })
#
#
# def my_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/')
#
#
# @my_login_required
# @require_http_methods(["GET"])
# def get(request):
#     user = request.user
#     user_name = user.get_username()
#     user_infos = user_manager.get_infos_json(user_name)
#     return api_response_data({
#         "user": user_infos,
#     }, SUCCESSFUL)
#
#

