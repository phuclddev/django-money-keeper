from services.models import Account
from common.utils import objects_to_json
from common import constants
from common.utils import dict_to_json
from common.logger import log
from django import forms


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['initial_balance', 'balance_name', 'balance_type', 'currency', 'description']

    def clean_initial_balance(self):
        initial_balance = self.cleaned_data['initial_balance']
        if initial_balance < 0:
            raise forms.ValidationError("Initial balance cannot be negative.")
        return initial_balance


def read_accounts_of_user(user):
    try:
        accounts = Account.objects.filter(user=user)
        temp_account_list = objects_to_json(accounts)
        return constants.ErrorCode.SUCCESS, temp_account_list
    except:
        log.error('Error while reading accounts of User %s', user.id)
        return constants.ErrorCode.ERROR_UNKNOWN, None


def create_accounts_of_user(user, body):
    try:
        form = AccountForm(body)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = user
            account.save()
            temp_account_list = dict_to_json(account.as_dict())
            return constants.ErrorCode.SUCCESS, temp_account_list
        else:
            errors = form.errors.as_json()
            return errors, None
    except:
        log.error('Error while creating accounts of User %s', user.id)
        return constants.ErrorCode.ERROR_UNKNOWN, None


def update_accounts_of_user(user, body, account_id):
    try:
        account = Account.objects.get(user=user, id=account_id)
    except Account.DoesNotExist:
        return constants.ErrorCode.ERROR_ACCOUNT_NOT_EXISTED, None
    form = AccountForm(body, instance=account)
    if form.is_valid():
        form.save()
        temp_account_list = dict_to_json(account.as_dict())
        return constants.ErrorCode.SUCCESS, temp_account_list
    else:
        errors = form.errors.as_json()
        return errors, None


def delete_accounts_of_user(user, account_id):
    try:
        account = Account.objects.get(user=user, id=account_id)
    except:
        return constants.ErrorCode.ERROR_UNKNOWN
    account.delete()
    return constants.ErrorCode.SUCCESS