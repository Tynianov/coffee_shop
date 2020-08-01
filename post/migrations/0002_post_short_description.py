# Generated by Django 2.2.14 on 2020-08-01 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='short_description',
            field=models.TextField(blank=True, default='', help_text='Set post short description to show on post preview', verbose_name='Short description'),
        ),
    ]
