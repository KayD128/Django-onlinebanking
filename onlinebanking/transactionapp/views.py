from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Account_table, Transaction_table, Future_transaction_table
from .forms import Deposit_form, PinAuthentication_form, Change_pin_form, Future_transaction_form
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models import F
from numpy import random
import threading, datetime
# Create your views here.

message=""
acct_number = 0

@login_required
@transaction.atomic
def deposit(request, user_id):
    # print(user_id)
    if request.method == 'POST':
    #     # user_acct = get_object_or_404(Account_table, user_id=user_id)   # TO get the account model
        user_form = Deposit_form(request.POST)
        if user_form.is_valid():
            acct_num = user_form.cleaned_data['your_account']
            amount = user_form.cleaned_data['amount']
            # with transaction.atomic():
                # To update table, we type:
            Account_table.objects.filter(account_number=acct_num).update(account_balance = F('account_balance') + amount)

            userAccount = Account_table.objects.filter(account_number=acct_num).values()[0]
            # Befr you can access any field, convert to dictionary first with .values()
            # print(userAccount)

            transact = Transaction_table(user_id=user_id, account_id=userAccount.get("account_id"), transaction_type="deposit", account_number=acct_num, transaction_amount=amount)
            transact.save()
            
            messages.success(request, ('Your deposit ' + str(amount)+ ' was successful. Your Total Balance is ' + str(userAccount.get("account_balance"))))
        else:
            messages.error(request, ("Your transaction failed"))
        return HttpResponsePermanentRedirect(reverse('deposit', args=(user_id,)))
    else:
        # user_acct = get_object_or_404(Account_table, user_id=user_id)
        deposit_form = Deposit_form()
        return render(request, 'transactionapp/deposit_form.html', {
        'deposit_form': deposit_form})
            
@login_required
def pinAuthentication(request, action):
    global acct_number
    # user_operation = action
    if request.method=='POST':
        pin_form = PinAuthentication_form(request.POST)
        if pin_form.is_valid():
            acct_number = pin_form.cleaned_data["your_account"]   #  The one in bracket is gotten from variable in ur form
            acct_pin = pin_form.cleaned_data["pin"]
        user_account = Account_table.objects.filter(account_number = acct_number, account_pin=acct_pin)
        if user_account:
            return HttpResponsePermanentRedirect(reverse('transaction', args=(action,)))
        else:
            messages.error(request, ("Your account number and pin don't match, Please try again"))
            return HttpResponsePermanentRedirect(reverse(action, args=(action,)))
    else:
        pin_form = PinAuthentication_form()
    return render(request, 'transactionapp/pin_auth_form.html', {'pin_form': pin_form})

@transaction.atomic
def general_transaction(request, action):
    global message
    if request.method == 'POST':
        # user_acct = get_object_or_404(Account_table, user_id=user_id)   # TO get the account model
        user_form = Deposit_form(request.POST)
        if user_form.is_valid():
            benefit_acct = user_form.cleaned_data["beneficiary_account"]
            benefit_bank = user_form.cleaned_data["beneficiary_bank"]
            bill_type = user_form.cleaned_data["bill_type"]
            amount = user_form.cleaned_data['amount']
            benefit_number = user_form.cleaned_data['beneficiary_number']

            #  To check which is filled between the beneficiary account or the number
            if benefit_acct:
                benefit_num = benefit_acct
            else:
                benefit_num = benefit_number
            account_balance = Account_table.objects.filter(user_id=request.user.id, account_number=acct_number).values()[0]
            if account_balance.get("account_balance") > amount:
                if action == "withdraw":
                    # To update table, we type:
                    Account_table.objects.filter(user_id=request.user.id, account_number=acct_number).update(account_balance = F('account_balance') - amount)
                elif action == "pay_bill":
                    Account_table.objects.filter(user_id=request.user.id, account_number=acct_number).update(account_balance = F('account_balance') - amount)

                    # TO generate a dummy acct number gfor bill payment
                    bill_number = "22"+str(random.randint(00000000, 99999999))
                    message = "Your "+ bill_type + " transaction code is "+ str(bill_number)
                elif action == "transfer":
                    Account_table.objects.filter(user_id=request.user.id, account_number=acct_number).update(account_balance = F('account_balance') - amount)

                    Account_table.objects.filter(account_number=benefit_acct).update(account_balance = F('account_balance') + amount)

                elif action == "recharge":
                    Account_table.objects.filter(user_id=request.user.id, account_number=acct_number).update(account_balance = F('account_balance') - amount)
                    message = "Your recharge of " + amount +"was successful."
                else:
                    messages.error(request, ("This transaction is not available for now."))
                    return HttpResponsePermanentRedirect(reverse(action, args=(action,)))
            else:
                messages.error(request, ("Insufficient balance."))
                return HttpResponsePermanentRedirect(reverse(action, args=(action,)))

            # Insert customer's transaction into transaction table for reference
            userAccount = Account_table.objects.filter(user_id=request.user.id, account_number=acct_number).values()[0]
            
            # Befr you can access any field, convert to dictionary first with .values()

            # print(userAccount)
            # Equate ur model name to ur form done here
            transact = Transaction_table(user_id=userAccount.get("user_id"), transaction_type=action,account_id=userAccount.get("account_id"), account_number=acct_number, transaction_amount=amount, recipient_bank=benefit_bank,recipient_number=benefit_num)
            recipient = Transaction_table(user_id=userAccount.get("user_id"), transaction_type=action,account_id=userAccount.get("account_id"), account_number=benefit_num, transaction_amount=amount, recipient_bank=benefit_bank,recipient_number=acct_number)
            transact.save()
            recipient.save()
            messages.success(request, ('Your transaction ' + str(amount)+ ' was successful. \n Your Total Balance is ' + str(userAccount.get("account_balance"))+message))
        else:
            messages.error(request, ("Your transaction failed"))
        return HttpResponsePermanentRedirect(reverse(action, args=(action,)))
    else:
        # user_acct = get_object_or_404(Account_table, user_id=user_id)
        deposit_form = Deposit_form()
        return render(request, 'transactionapp/deposit_form.html', {
        'deposit_form': deposit_form, 'action':action, 'account_num': acct_number})

@login_required
def changePin(request, account_num):
    if request.method=='POST':
        pin_form = Change_pin_form(request.POST)
        if pin_form.is_valid():
            oldPin = pin_form.cleaned_data["old_pin"]   #  The one in bracket is gotten from variable in ur form
            newPin = pin_form.cleaned_data["new_pin"]
            confirmPin = pin_form.cleaned_data["new_pin2"]
        user_account = Account_table.objects.filter(account_number=account_num, account_pin=oldPin)
        if user_account and newPin == confirmPin:
            Account_table.objects.filter(user_id=request.user.id, account_number=account_num).update(account_pin=newPin)
            messages.success(request, ("Your PIN has been updated successfully"))
            return HttpResponsePermanentRedirect(reverse('display_account', args=(request.user.id,)))
        else:
            messages.error(request, ("Your PIN is not correct, Please try again"))
            return HttpResponsePermanentRedirect(reverse('display_account', args=(request.user.id,)))
    else:
        pin_form = Change_pin_form()
    return render(request, 'transactionapp/change_pin.html', {'pin_form': pin_form})

@login_required
def displayAccount(request, user_id):
    user_account = Account_table.objects.all().filter(user_id=user_id)
# .only("account_number", 'account_type', 'account_balance')
    return render(request, 'transactionapp/show_accounts.html', {
        'user_account': user_account})

@login_required
def accountStatement(request, account_num):
    account_statement = Transaction_table.objects.all().filter(account_number=account_num)
    # print(account_statement)
    return render(request, 'transactionapp/account_statement.html', {
        'account_statement': account_statement})

@login_required
def accountBalance(request, account_num):
    user_account = Account_table.objects.only("account_balance").filter(account_number=account_num)
    # print(user_account.values())
# .only("account_number", 'account_type', 'account_balance')
    messages.success(request, ("Your account balance is "+str(user_account.values()[0].get("account_balance"))))
    return render(request, 'transactionapp/show_accounts.html', {
        'user_account': user_account})

@login_required
# @transaction.atomic
def futureTransaction(request, account_num):
    if request.method=='POST':
        future_form = Future_transaction_form(request.POST)
        if future_form.is_valid():
            benefit_acct = future_form.cleaned_data["beneficiary_account"]
            benefit_bank = future_form.cleaned_data["beneficiary_bank"]
            bill_type = future_form.cleaned_data["bill_type"]
            amount = future_form.cleaned_data['amount']
            fdate = future_form.cleaned_data['future_date']
            ftime = future_form.cleaned_data['future_time']

            future_trans = Future_transaction_table( transaction_type=bill_type, user_id=request.user.id, owner_account=account_num, transaction_amount=amount, recipient_bank=benefit_bank,recipient_account=benefit_acct, future_date=fdate, future_time=ftime)
            future_trans.save()

            messages.success(request, ('Your future transaction for ' + str(account_num)+ ' was successful.'))
            return HttpResponsePermanentRedirect(reverse('display_account', args=(account_num,)))
        else:
            messages.error(request, ("Your transaction failed"))
            return HttpResponsePermanentRedirect(reverse('future_trans', args=(account_num,)))
    else:
        future_form = Future_transaction_form()
    return render(request, 'transactionapp/future_transaction_form.html', {'future_form': future_form})

def startFutureTransaction():
    while True:
        tim = datetime.datetime.now()
        today_date = tim.date()
        #  "2022-07-26"
        today_time = str(tim.strftime("%H")+"-"+str(tim.strftime("%M"))+"-"+str(tim.strftime("%S")))
        # tim.time()
        all_account = Future_transaction_table.objects.all().values()
        # print(all_account)
        for key in all_account:
            
            account_balance = Account_table.objects.filter(user_id=key["user_id"], account_number=key["owner_account"])
            if key["future_date"] == today_date and key["future_time"] == today_time:
                # print("transaction successful")
                account_balance = Account_table.objects.filter(user_id=key["user_id"], account_number=key["owner_account"]).values()[0]

                Future_transaction_table.objects.filter(user_id=key["user_id"], owner_account=key["owner_account"]).update(future_date=datetime.datetime(tim.year, tim.month+1, 25))

                if account_balance.get("account_balance") > key["transaction_amount"]:
                    Account_table.objects.filter(user_id=key["user_id"], account_number=key["owner_account"]).update(account_balance = F('account_balance') - key["transaction_amount"])

                    Account_table.objects.filter(account_number=key["recipient_account"]).update(account_balance = F('account_balance') + key["transaction_amount"])

                    userAccount = Account_table.objects.filter(user_id=key["user_id"], account_number=key["owner_account"]).values().last()
                
                    transact = Transaction_table(transaction_type="Future" + key["transaction_type"],account_id=userAccount.get("account_id"), account_number=key["owner_account"], transaction_amount="Future" + key["transaction_amount"], recipient_bank=key["recipient_bank"],recipient_number=key["recipient_account"])

                    recipient = Transaction_table(user_id=userAccount.get("user_id"), transaction_type="Future" + key["transaction_type"], account_id=userAccount.get("account_id"), account_number=key["recipient_account"], transaction_amount="Future" + key["transaction_amount"], recipient_bank=key["recipient_bank"], sender_account=key["owner_account"])
                    transact.save()
                    recipient.save()

transaction_thread = threading.Thread(target=startFutureTransaction, name = 'trans_thread', daemon=True)
transaction_thread.start()