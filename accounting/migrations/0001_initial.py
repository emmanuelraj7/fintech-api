# Generated by Django 2.1.2 on 2018-10-21 22:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('card_id', models.CharField(max_length=20, unique=True)),
                ('currency', models.CharField(max_length=3)),
                ('total_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reserved_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=30)),
                ('card_id', models.IntegerField()),
                ('total_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('transaction_id', models.CharField(max_length=20, unique=True)),
                ('type', models.CharField(max_length=16)),
                ('merchant_name', models.CharField(max_length=255)),
                ('merchant_country', models.CharField(max_length=4)),
                ('merchant_city', models.CharField(default=None, max_length=128, null=True)),
                ('merchant_mcc', models.IntegerField()),
                ('billing_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('billing_currency', models.CharField(max_length=3)),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_currency', models.CharField(max_length=3)),
                ('settlement_amount', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('settlement_currency', models.CharField(default=None, max_length=3, null=True)),
                ('settled', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Accounts', to_field='card_id')),
            ],
        ),
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('transfer_type', models.CharField(choices=[('CRT', 'Credit'), ('DBT', 'Debit')], max_length=3)),
                ('total_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Accounts')),
                ('transaction', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.Transactions', to_field='transaction_id')),
            ],
        ),
        migrations.AddField(
            model_name='accounts',
            name='customer_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Customers'),
        ),
    ]
