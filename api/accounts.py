from django.views.decorators.csrf import csrf_exempt
from services.accounts import account_manager
from .schema import *
from common.decorator import *
from common.logger import log
from common import constants
from django.views.decorators.http import require_http_methods


@csrf_exempt
@my_login_required
@require_http_methods(["GET", "POST"])
@parse_params(account_schema, ['POST'])
def list(request, body):
    user = request.user
    if request.method == 'GET':
        error_code, temp_account_list = account_manager.read_accounts_of_user(user)
        if error_code != constants.ErrorCode.SUCCESS:
            return api_response_data({'error_code': error_code})
        log.info('Get account list successfully. User Id: %s', user.id)
        return api_response_data({
            "accounts_read": temp_account_list,
        }, SUCCESSFUL)
    elif request.method == 'POST':
        error_code, temp_account_list = account_manager.create_accounts_of_user(user, body)
        if error_code != constants.ErrorCode.SUCCESS:
            return api_response_data({'error_code': error_code})
        log.info('Get account list successfully. User Id: %s', user.id)
        return api_response_data({
            "account_create": temp_account_list,
        }, SUCCESSFUL)



@csrf_exempt
@my_login_required
@require_http_methods(["PUT", "DELETE"])
@parse_params(account_update_schema, ['PUT', 'DELETE'])
def detail(request, body, account_id):
    user = request.user
    if request.method == 'PUT':
        error_code, temp_account_list = account_manager.update_accounts_of_user(user, body, account_id)
        if error_code != constants.ErrorCode.SUCCESS:
            return api_response_data({'error_code': error_code})
        log.info('Put account list successfully. User Id: %s', user.id)
        return api_response_data({
            "accounts_update": temp_account_list,
        }, SUCCESSFUL)
    elif request.method == 'DELETE':
        error_code = account_manager.delete_accounts_of_user(user, account_id)
        if error_code != constants.ErrorCode.SUCCESS:
            return api_response_data({'error_code': error_code})
        log.info('Delete account list successfully. User Id: %s', user.id)
        return api_response_data({
        }, SUCCESSFUL)
