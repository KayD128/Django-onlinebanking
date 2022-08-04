# Generated by Django 4.0.5 on 2022-07-23 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactionapp', '0004_transaction_table_sender_account_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Future_transaction_table',
            fields=[
                ('future_id', models.AutoField(primary_key=True, serialize=False)),
                ('owner_account', models.CharField(max_length=10)),
                ('recipient_account', models.CharField(max_length=10)),
                ('recipient_bank', models.CharField(max_length=20, null=True)),
                ('transaction_type', models.CharField(max_length=20)),
                ('transaction_amount', models.BigIntegerField(null=True)),
                ('future_date', models.DateField()),
                ('future_time', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
