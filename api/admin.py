from django.contrib import admin
from services.models import User, Account, Transaction, Bank, Term, Saving, Image


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'account_type')
    list_filter = ('is_active', 'is_staff', 'account_type')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'avatar', 'phone_number', 'date_of_birth', 'gender', 'address', 'occupations',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Account', {'fields': ('account_type',)}),
    )
    readonly_fields = ('last_login', 'date_joined')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance_name', 'balance_type', 'initial_balance', 'currency', 'description')
    list_filter = ('balance_type', 'currency')
    search_fields = ('balance_name', 'description')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'type', 'amount', 'category', 'time')
    list_filter = ('type', 'category', 'time', 'account__balance_type', 'account__currency')
    search_fields = ('account__balance_name', 'type', 'category', 'description')
    readonly_fields = ('time',)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank_code', 'bank_name')
    search_fields = ('bank_code', 'bank_name')


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration_days')
    search_fields = ('name',)


@admin.register(Saving)
class SavingAdmin(admin.ModelAdmin):
    list_display = ('id', 'initial_balance')


@admin.register(Image)
class SavingAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_name')