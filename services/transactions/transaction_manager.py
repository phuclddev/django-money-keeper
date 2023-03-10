from services.models import Transaction
from common.utils import objects_to_json
from common import constants
from common.utils import dict_to_json
from common.logger import log
from django import forms


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'description']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError("Amount can't be negative.")
        return amount

    def clean_type(self):
        transaction_type = self.cleaned_data['type']
        valid_types = [t[0] for t in Transaction.TRANSACTION_TYPES]
        if transaction_type not in valid_types:
            raise forms.ValidationError("Invalid transaction type.")
        return transaction_type

    def clean_category(self):
        category = self.cleaned_data['category']
        valid_categories = [c[0] for c in Transaction.CATEGORIES]
        if category not in valid_categories:
            raise forms.ValidationError("Invalid category.")
        return category


def read_transactions_of_account(user, account):
    try:
        transactions = Transaction.objects.filter(account=account, user=user)
        temp_transactions_list = objects_to_json(transactions)
        return constants.ErrorCode.SUCCESS, temp_transactions_list
    except:
        log.error('Error while reading accounts of User %s', user.id)
        return constants.ErrorCode.ERROR_UNKNOWN, None


def create_transactions_of_account(user, account, body):
    try:
        form = TransactionForm(body)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = user
            transaction.account = account
            transaction.save()
            temp_transaction_list = dict_to_json(transaction.as_dict())
            return constants.ErrorCode.SUCCESS, temp_transaction_list
        else:
            errors = form.errors.as_json()
            return errors, None
    except:
        log.error('Error while creating transactions of User %s', user.id)
        return constants.ErrorCode.ERROR_UNKNOWN, None


def update_transaction_of_user(user, body, transaction_id):
    try:
        transaction = Transaction.objects.get(user=user, id=transaction_id)
    except Transaction.DoesNotExist:
        return constants.ErrorCode.ERROR_TRANSACTION_NOT_EXISTED, None
    form = TransactionForm(body, instance=transaction)
    if form.is_valid():
        form.save()
        temp_transaction_list = dict_to_json(transaction.as_dict())
        return constants.ErrorCode.SUCCESS, temp_transaction_list
    else:
        errors = form.errors.as_json()
        return errors, None


def delete_transaction_of_user(user, transaction_id):
    try:
        transaction = Transaction.objects.get(user=user, id=transaction_id)
    except:
        return constants.ErrorCode.ERROR_UNKNOWN
    transaction.delete()
    return constants.ErrorCode.SUCCESS