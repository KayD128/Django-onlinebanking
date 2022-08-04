from django.shortcuts import render, get_object_or_404
from .forms import SignUpForm, Staff_form, User_form, Account_Open_form
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from .models import profile
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
# from django.core.mail import send_mail
from onlinebanking.transactionapp.models import Account_table
from numpy import random

# Create your views here.
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def manage_staff(request):
    staff_details = profile.objects.all().filter(staff=True)
    return render(request, 'staffapp/manage_staff.html',
    {'staff':staff_details})

@login_required
def manage_customer(request):
    customer_details = profile.objects.all().filter(staff=False)
    return render(request, 'staffapp/manage_customer.html',
    {'customer':customer_details})

@login_required
def staff_profile(request, user_id):
    profile_details = profile.objects.all().filter(user_id=user_id)
    return render(request, 'staffapp/staff_profile.html',
    {'profile_details':profile_details})

@login_required
@transaction.atomic
def edit_profile(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)  # only if it is a user form
        user_form = User_form(request.POST, instance=user) # We will need user instance cos we have filled them befr and need that info
        profile_form = Staff_form(request.POST or None, request.FILES or None, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
           
            user_form.save()
            profile_form.save()
            if profile_form.cleaned_data['staff']:
                user.is_staff = True
                user.save()
            else:
                user.is_staff = False
                user.save()
            messages.success(request, ('Your profile was successfully updated!'))
            staff_profile(request, user_id)
        else:
            messages.error(request, ('Please correct the error below.'))
            return HttpResponsePermanentRedirect(reverse('edit_profile', args=(user_id,)))
    else:
        user = get_object_or_404(User, id=user_id)
        user_form = User_form(instance=user)
        profile_form = Staff_form(instance=user.profile)
    return render(request, 'staffapp/staff_edit_profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form     
    })
            

@login_required
# @permission_required('User.is_superuser')
def deactivate_staff(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = 0
    else:
        user.is_active = 1
    user.save()
    # return HttpResponsePermanentRedirect(reverse('staff_profile', args=(user_id,)))
    return staff_profile(request, user_id)

@login_required
def create_user_account(request, user_id):
        # user_info = profile.objects.filter(id=user_id)
        user_acct_number = Account_table.objects.filter(user_id=user_id)
        if request.method == 'POST':
            account_form = Account_Open_form(request.POST)
            user_info = profile.objects.filter(id=user_id)
            if account_form.is_valid():
                acct_type = account_form.cleaned_data['account_type']
                acct_balance = account_form.cleaned_data['account_balance']
                open_account = Account_table(account_type=acct_type, account_balance=acct_balance)
                open_account.user_id = user_id
                open_account.account_pin = 1111
                if user_acct_number:
                    open_account.account_number = "22"+str(random.randint(00000000, 99999999))
                else:
                    open_account.account_number = user_info.values()[0]["account_number"]   
                open_account.save()
                messages.success(request, ('Your account was created successfully!'))
                return staff_profile(request, user_id)
            else:
                messages.error(request, ("Please correct the error below."))
                return HttpResponsePermanentRedirect(reverse('create_account', args=(user_id,)))
        else:
            account_form = Account_Open_form()
            return render(request, 'transactionapp/create_account.html', {'form': account_form})

