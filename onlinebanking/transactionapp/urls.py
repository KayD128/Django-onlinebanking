from django.contrib import admin
from django.urls import re_path
from onlinebanking.transactionapp import views as trans_view

urlpatterns = [
    re_path(r'^deposit/(?P<user_id>\d+)/', trans_view.deposit, name='deposit'),
    re_path(r'^withdraw/(?P<action>\D+)/', trans_view.pinAuthentication, name='withdraw'),
    re_path(r'^pay_bill/(?P<action>\D+)/', trans_view.pinAuthentication, name='pay_bill'),
    re_path(r'^transfer/(?P<action>\D+)/', trans_view.pinAuthentication, name='transfer'),
    re_path(r'^recharge/(?P<action>\D+)/', trans_view.pinAuthentication, name='recharge'),
    re_path(r'^transaction/(?P<action>\D+)/', trans_view.general_transaction, name='transaction'),
    re_path(r'^change_pin/(?P<account_num>\d+)/', trans_view.changePin, name='change_pin'),
    re_path(r'^display_account/(?P<user_id>\d+)/', trans_view.displayAccount, name='display_account'),
    re_path(r'^future_trans/(?P<account_num>\d+)/', trans_view.futureTransaction, name='future_trans'),
    re_path(r'^check_balance/(?P<account_num>\d+)/', trans_view.accountBalance, name='balance'),
    re_path(r'^account_statement/(?P<account_num>\d+)/', trans_view.accountStatement, name='account_statement'),
]
