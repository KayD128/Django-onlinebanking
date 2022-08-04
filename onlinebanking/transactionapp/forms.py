from django import forms
from .models import Account_table

class GeneralParam():
    def get_account(self):
        account_list = [("", "-----")]
        account_num = Account_table.objects.all().values()
        for account in account_num:
            account_list.append((account['account_number'], account['account_number']))
        return account_list

    bank_name = [
        ("", "-----"),
        ("FBN", "First bank of Nigeria"),
        ("FCMB", "FCMB"),
        ("GTB", "GTB"),
        ("UBA", "UBA")
    ]

    bill_type2 = [
        ("", "-----"),
        ("PHCN", "PHCN"),
        ("DSTV", "DSTV"),
        ("GOTV", "GOTV"),
    ]
    
    mobile_network2 = [
        ("", "-----"),
        ("MTN", "MTN"),
        ("GLO", "GLO"),
        ("AIRTEL", "AIRTEL"),
        ("ETISALAT", "ETISALAT"),
    ]


class Deposit_form(forms.Form):
    # amount = forms.IntegerField()
    # class Meta:
    #     model = Account_table
    #     fields = [
    #         "account_number",
    #         "amount"
    #     ]
    param = GeneralParam()
    your_account = forms.ChoiceField(choices=param.get_account(), label="Your Account Number", required=False)

    beneficiary_account = forms.ChoiceField(choices=param.get_account(), label="Beneficiary Account Number", required=False)

    bill_type = forms.ChoiceField(choices=param.bill_type2, label="Type of Bill", required=False)

    beneficiary_bank = forms.ChoiceField(choices=param.bank_name, label="Bank", required=False)
    # , widget=forms.ChoiceField(attrs={'placeholder': 'Beneficiary Bank'})
    amount = forms.IntegerField(label="Amount", required=False)
    # , widget=forms.TextInput(attrs={'placeholder': 'Amount'}),
    beneficiary_number = forms.CharField(label="", required=False)
    # widget=forms.NumberInput(attrs={'placeholder': 'Beneficiary number'}),
    mobile_network = forms.ChoiceField(choices=param.mobile_network2, label="Network", required=False)
    # widget=forms.ChoiceField(attrs={'placeholder': 'Beneficiary Bank'}),

class PinAuthentication_form(forms.Form):
    param = GeneralParam()
    your_account = forms.ChoiceField(choices=param.get_account(), label="Your Account Number")
    pin = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Enter your pin'}), label="")

class Change_pin_form(forms.Form):
    old_pin = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter your old PIN'}), label="")
    new_pin = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter your new PIN'}), label="")
    new_pin2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm PIN'}), label="")

class Future_transaction_form(forms.Form):
    bill_type2 = [
        ("", "-----"),
        ("SALARY", "SALARY"),
        ("PHCN", "PHCN"),
        ("DSTV", "DSTV"),
        ("GOTV", "GOTV"),
    ]
    param = GeneralParam()
    beneficiary_account = forms.ChoiceField(choices=param.get_account(), label="Beneficiary Account Number", required=False)

    bill_type = forms.ChoiceField(choices=bill_type2, label="Type of Bill", required=False)

    beneficiary_bank = forms.ChoiceField(choices=param.bank_name, label="Bank", required=False,)
    # , widget=forms.ChoiceField(attrs={'placeholder': 'Beneficiary Bank'})
    amount = forms.IntegerField(label="Amount")
    # , widget=forms.TextInput(attrs={'placeholder': 'Amount'}),
    future_date = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))
    future_time = forms.TimeField(widget=forms.NumberInput(attrs={'type': 'time'}))
