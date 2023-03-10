from django.urls import path
from api import users, accounts, transactions

app_name = 'api'
urlpatterns = [
    path('user/detail/', users.detail),
    path('account/', accounts.list),
    path('account/<int:account_id>/', accounts.detail),
    path('account/<int:account_id>/transaction/', transactions.list),
    path('account/<int:account_id>/transaction/<int:transaction_id>/', transactions.detail),
    path('account/<int:account_id>/transaction/<int:transaction_id>/upload', transactions.upload),
    # To-do
    # Saving part
]