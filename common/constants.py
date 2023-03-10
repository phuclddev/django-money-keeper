from django.utils import timezone

CURRENT_TIME = timezone.now()
SUCCESSFUL = 'successful'
FAIL = 'fail'


class ErrorCode(object):
    SUCCESS = 'success'
    ERROR_INVALID_CREDENTIALS = 'error_invalid_credentials'
    ERROR_PHONE_NUMBER = 'error_phone_number_format'
    ERROR_UNKNOWN = 'error_unknown'
    ERROR_DATE_OF_BIRTH = 'error_date_of_birth_format'
    ERROR_NOT_LOGGED_IN = 'error_not_logged_in'
    ERROR_ACCOUNT_NOT_EXISTED = 'error_account_not_existed'
    ERROR_TRANSACTION_NOT_EXISTED = 'transaction_not_existed'
    ERROR_BASIC_ACCOUNT = 'error_basic_account'
    ERROR_PARAMS = 'error_params'
    ERROR_SERVER = 'error_server'
    ERROR_INVALID_FILE_TYPE = 'error_invalid_file_type'
    ERROR_CONFIG = 'error_config'
