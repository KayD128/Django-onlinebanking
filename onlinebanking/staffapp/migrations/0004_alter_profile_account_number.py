# Generated by Django 4.0.5 on 2022-07-14 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffapp', '0003_alter_profile_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_number',
            field=models.BigIntegerField(default='2270548102', unique=True),
        ),
    ]
