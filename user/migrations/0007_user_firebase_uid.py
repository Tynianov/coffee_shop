# Generated by Django 2.2.14 on 2020-08-31 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20200824_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firebase_uid',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Firebase user uId'),
        ),
    ]
