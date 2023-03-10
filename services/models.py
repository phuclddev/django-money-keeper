from datetime import date as date_type, time as time_type
from django.db.models.fields.related import ManyToManyField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
import os


if settings.DB_TABLE_PREFIX == '':
    raise Exception('Invalid settings.DB_TABLE_PREFIX')


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def as_dict(self, fields=None, exclude=None):
        opts = self._meta
        data = {}
        fs = list(opts.fields) + list(opts.many_to_many)
        for f in fs:
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            else:
                data[f.name] = f.value_from_object(self)
        return data

    def as_json(self, fields=None, exclude=None, **kwargs):
        """
        Return a JSON-dumpable dict
        """
        data = self.as_dict(fields, exclude)
        for attr in data:
            if isinstance(data[attr], time_type):
                data[attr] = data[attr].strftime(kwargs.get('time_format', '%H:%M:%S'))
            elif isinstance(data[attr], date_type):
                data[attr] = data[attr].strftime(kwargs.get('date_format', '%Y-%m-%d %H:%M:%S'))
            elif isinstance(data[attr], FieldFile):
                file_data = {}
                for k in kwargs.get('file_attributes', ('url',)):
                    file_data[k] = data[attr].__getattribute__(k) if hasattr(data[attr], k) else ''
                data[attr] = file_data
        return data

    def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
        return super()._do_update(base_qs, using, pk_val, values, update_fields, forced_update)


class User(BaseModel, AbstractUser):
    class Meta:
        db_table = settings.DB_TABLE_PREFIX + '_user'
        verbose_name = 'Users'

    TYPES = (
        (1, 'Basic'),
        (2, 'Premium')
    )
    avatar = models.CharField('Avatar', max_length=256, default='', editable=True)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True,
                                    validators=[RegexValidator(regex='^[0-9]{5,13}$',
                                                               message='Phone number must be between 5 and 13 digits')])
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    occupations = models.CharField(max_length=255, null=True, blank=True)
    account_type = models.IntegerField('Type', default=1, choices=TYPES)

    def check_type(self):
        if self.type == 2:
            return True
        else:
            return False

    def as_dict(self, fields=None, exclude=None):
        res = BaseModel.as_dict(self, ['email', 'first_name', 'last_name', 'avatar', 'phone_number', 'date_of_birth',
                                       'gender', 'address', 'occupations', 'account_type', ])
        return res

    User._meta.get_field('is_active').verbose_name = 'Active'
    User._meta.get_field('is_superuser').verbose_name = 'Admin'


class Account(BaseModel, models.Model):
    BALANCE_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('bank_account', 'Bank account'),
        ('credit_card', 'Credit card'),
        ('investment', 'Investment'),
        ('e-wallet', 'E-wallet'),
        ('other', 'Other'),
    ]

    CURRENCY_CHOICES = [
        ('VND', 'Vietnam dong'),
        ('USD', 'United States Dollar'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_balance = models.DecimalField(max_digits=15, decimal_places=2)
    balance_name = models.CharField(max_length=255)
    balance_type = models.CharField(max_length=50, choices=BALANCE_TYPE_CHOICES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.balance_name

class Transaction(BaseModel, models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    LEND = 'lend'
    BORROW = 'borrow'
    TRANSFER = 'transfer'
    ADJUSTMENT = 'adjustment'

    TRANSACTION_TYPES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
        (LEND, 'Lend'),
        (BORROW, 'Borrow'),
        (TRANSFER, 'Transfer'),
        (ADJUSTMENT, 'Adjustment'),
    ]

    FOOD = 'food'
    UTILITIES = 'utilities'
    TRANSPORT = 'transport'
    CLOTHING = 'clothing'
    ENTERTAINMENT = 'entertainment'
    BANK = 'bank'
    GIFTS = 'gifts'
    PERSONAL = 'personal'
    SALARY = 'salary'
    BONUS = 'bonus'
    INTEREST = 'interest'
    OTHER = 'other'
    BORROW_COLLECTING_DEBTS = 'borrow_collecting_debts'

    CATEGORIES = [
        (FOOD, 'Food'),
        (UTILITIES, 'Utilities'),
        (TRANSPORT, 'Transport'),
        (CLOTHING, 'Clothing'),
        (ENTERTAINMENT, 'Entertainment'),
        (BANK, 'Bank'),
        (GIFTS, 'Gifts'),
        (PERSONAL, 'Personal'),
        (SALARY, 'Salary'),
        (BONUS, 'Bonus'),
        (INTEREST, 'Interest'),
        (OTHER, 'Other'),
        (BORROW_COLLECTING_DEBTS, 'Borrow/Collecting Debts'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORIES)
    description = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.account.balance_name

    class Meta:
        ordering = ['-time']

User._meta.get_field('groups').related_name = 'auth_groups'
User._meta.get_field('user_permissions').related_name = 'auth_user_permissions'


class Bank(BaseModel, models.Model):
    bank_code = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return self.bank_name


class Term(BaseModel, models.Model):
    name = models.CharField(max_length=255)
    duration_days = models.IntegerField()

    def __str__(self):
        return self.name


INTEREST_PAID_CHOICES = [
    ('up-front', 'Up-front'),
    ('maturity', 'Maturity'),
    ('monthly', 'Monthly')
]

TERM_ENDED_CHOICES = [
    ('rollover-principal-and-interest', 'Rollover principal and interest'),
    ('rollover-principal', 'Rollover principal'),
    ('close-account', 'Close account')
]

STATUS_CHOICES = [
    ('open', 'Open'),
    ('close', 'Close'),
    ('withdraw-partially', 'Withdraw partially')
]


class Saving(BaseModel, models.Model):
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)
    withdraw_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    saving_name = models.CharField(max_length=255)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    interest_paid = models.CharField(max_length=50, choices=INTEREST_PAID_CHOICES)
    term_ended = models.CharField(max_length=50, choices=TERM_ENDED_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)


def transaction_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/transaction_<id>/<filename>
    transaction_dir = f'transaction_{instance.transaction.id}'
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, transaction_dir)):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, transaction_dir))
    return os.path.join(transaction_dir, filename)


class Image(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=transaction_directory_path)
    image_name = models.CharField(max_length=255, default="default_name")


