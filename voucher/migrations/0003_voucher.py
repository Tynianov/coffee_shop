# Generated by Django 2.2.14 on 2020-07-22 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voucher', '0002_auto_20200719_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True, verbose_name='дата содания')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='Отметьте, если объект должен быть активным', verbose_name='Активен?')),
                ('is_scanned', models.BooleanField(default=False, verbose_name='Отсканирован?')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата истечения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to=settings.AUTH_USER_MODEL)),
                ('voucher_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='voucher.VoucherConfig')),
            ],
            options={
                'verbose_name': 'Ваучер',
                'verbose_name_plural': 'Ваучеры',
            },
        ),
    ]
