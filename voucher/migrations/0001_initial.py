# Generated by Django 2.2.14 on 2020-07-27 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VoucherConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='Designate, if object is active', verbose_name='Is active?')),
                ('name', models.CharField(help_text='Enter voucher name', max_length=256, verbose_name='Voucher name')),
                ('description', models.CharField(blank=True, default='', help_text='Enter voucher description', max_length=512, verbose_name='Voucher description')),
                ('type', models.CharField(choices=[('min_purchase_amount', 'Minimum purchase amount'), ('for_registration', 'For registration'), ('for_all_users', 'For all users')], default='min_purchase_amount', help_text='Select voucher type (in which case user receive voucher)', max_length=32, verbose_name='Voucher type')),
                ('discount', models.CharField(choices=[('fixed', 'Fixed discount'), ('percentage', 'Percentage dicount'), ('free_item', 'Free product')], default='fixed', help_text='Select discount type', max_length=32, verbose_name='Discount type')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Set discount amount', max_digits=8, verbose_name='Amount')),
                ('duration', models.PositiveIntegerField(blank=True, help_text='Set how much days will voucher be available after creation', null=True, verbose_name='Voucher duration')),
            ],
            options={
                'verbose_name': 'Voucher discount',
                'verbose_name_plural': 'Voucher discount',
            },
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='Designate, if object is active', verbose_name='Is active?')),
                ('is_scanned', models.BooleanField(default=False, verbose_name='Is scanned?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='Expiration date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to=settings.AUTH_USER_MODEL)),
                ('voucher_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='voucher.VoucherConfig')),
            ],
            options={
                'verbose_name': 'Voucher',
                'verbose_name_plural': 'Vouchers',
            },
        ),
    ]
