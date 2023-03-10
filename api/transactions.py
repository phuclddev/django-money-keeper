from django.views.decorators.csrf import csrf_exempt
from services.transactions import transaction_manager
from .schema import *
from common.decorator import *
from common.logger import log
from common import constants
from django.views.decorators.http import require_http_methods
from services.models import Account
import os
from services.models import Transaction, Image
import datetime

@csrf_exempt
@my_login_required
@require_http_methods(["GET", "POST"])
@parse_params(transaction_schema, ['POST'])
def list(request, body, account_id):
    user = request.user
    account = Account.objects.get(id=account_id)
    if request.method == 'GET':
        error_code, temp_transaction_list = transaction_manager.read_transactions_of_account(user, account)
        if error_code != constants.ErrorCode.SUCCESS:
            return api_response_data({'error_code': error_code})
        log.info('Read transaction list successfully. User Id: %s', user.id)
        return api_response_data({
            "transaction_read": temp_transaction_list,
        }, SUCCESSFUL)
    elif request.method == 'POST':
        error_code, temp_transaction_list = transaction_manager.create_transactions_of_account(user, account, body)
        if error_code != constants.ErrorCode.SUCCESS:
            return api_response_data({'error_code': error_code})
        log.info('Create transaction list successfully. User Id: %s', user.id)
        return api_response_data({
            "transaction_create": temp_transaction_list,
        }, SUCCESSFUL)


@csrf_exempt
@my_login_required
@require_http_methods(["POST"])
def upload(request, account_id, transaction_id):
    uploaded_files = request.FILES.getlist("images")
    transaction = Transaction.objects.get(id=transaction_id)
    image_urls = []
    for i, uploaded_file in enumerate(uploaded_files):
        now = datetime.datetime.now()
        time_string = now.strftime("%Y%m%d%H%M%S")
        filename = f"{transaction_id}__{time_string}_{i}.jpg"
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, str(transaction_id))):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, str(transaction_id)))
        file_path = os.path.join(settings.MEDIA_ROOT, str(transaction_id), filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        image = Image(transaction=transaction, image=file_path, image_name=filename)
        image.save()
        image_url = request.build_absolute_uri(image.image.url)
        image_urls.append(image_url)
    return api_response_data({
        "image_url": image_urls,
    }, SUCCESSFUL)


@csrf_exempt
@my_login_required
@require_http_methods(["PUT", "DELETE"])
@parse_params(transaction_update_schema, ['PUT', 'DELETE'])
def detail(request, body, account_id, transaction_id):
    user = request.user
    if request.method == 'PUT':
        error_code, temp_transaction_list = transaction_manager.update_transaction_of_user(user, body, transaction_id)
        if error_code != constants.ErrorCode.SUCCESS:
            return api_response_data({'error_code': error_code})
        log.info('Put transaction list successfully. User Id: %s', user.id)
        return api_response_data({
            "transaction_update": temp_transaction_list,
        }, SUCCESSFUL)
    elif request.method == 'DELETE':
        error_code = transaction_manager.delete_transaction_of_user(user, transaction_id)
        if error_code != constants.ErrorCode.SUCCESS:
            return api_response_data({'error_code': error_code})
        log.info('Delete transaction successfully. User Id: %s', user.id)
        return api_response_data({
        }, SUCCESSFUL)
