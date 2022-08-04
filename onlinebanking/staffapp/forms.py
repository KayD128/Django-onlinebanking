from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from onlinebanking.transactionapp.models import Account_table
from .models import profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

class User_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

# Can call "staff_Form" any name

class Staff_form(forms.ModelForm):
    profile_passport = forms.ImageField(required=False, label='Profile passport')
    means_of_identity = forms.ImageField(required=False, label='Means of identity')
    particulars = forms.FileField(required=False, label='particulars')
    class Meta:
        model = profile
        fields = [
            'status',
            'address',
            'phone',
            'nationality',
            'state',
            'means_of_identity',
            'particulars',
            'profile_passport',
            'position',
            'marital_status',
            'staff',
        ]

class Account_Open_form(forms.Form):
    account_type = [
        ("Savings", "Savings"),
        ("Current", "Current"),
        ("Fixed Deposit", "Fixed Deposit"),
    ]

    account_balance = forms.IntegerField()
    account_type = forms.ChoiceField(choices=account_type)

    