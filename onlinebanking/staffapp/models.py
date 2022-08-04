from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from numpy import random


# Create your models here.
class profile(models.Model):
    countries = [
        ("Nigeria", "NIgeria"),
        ("Ghana", "Ghana"),
        ("United Kingdom", "UK"),
        ("USA", "USA")
    ]

    states = [
        ("Abia", "Abia"),
        ("Oyo", "Oyo"),
        ("Osun", "Osun"),
        ("Lagos", "Lagos"),
        ("Kano", "Kano"),
        ("Abuja", "Abuja"),
    ] 

    position = [
        ("CEO", "CEO"),
        ("GMD", "GMD"),
        ("CTO", "CTO"),
        ("Supervisor", "Supervisor"),
        ("Accountant", "Accountant"),
        ("Marketer", "Marketer"),
        ("Staff", "Staff"),
        ("HR", "HR"),    
    ]
    ma_status = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Divorce", "Divorce"),
        ("Complicate", "Complicate")
    ]

    account = "22"+str(random.randint(00000000, 99999999))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(unique=False, max_length=100, null=True)
    address = models.CharField(unique=False, max_length=100, null=True)
    phone = models.CharField(unique=True, max_length=11, null=True)
    nationality = models.CharField(choices=countries, unique=False, max_length=50, null=True)
    state = models.CharField(choices=states, unique=False, max_length=20, null=True)
    means_of_identity = models.ImageField(upload_to='identityImage/', unique=False, null=True)
    particulars = models.FileField(upload_to='particularsImage/',unique=False, null=True)
    profile_passport = models.ImageField(upload_to='staffImage/', unique=False, null=True)
    position = models.CharField(choices=position, unique=False, max_length=20, null=True)
    marital_status = models.CharField(choices=ma_status, unique=False, max_length=20, null=True)
    staff = models.BooleanField(default=False, unique=False)
    account_number = models.BigIntegerField(default=account, unique=True    )

# Now this is where the magic happens: we will now define signals so our profile model will be automatically created upon when we create/update User instances
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
