# Generated by Django 4.0.5 on 2022-07-14 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_number',
            field=models.BigIntegerField(default='2242411893'),
        ),
    ]