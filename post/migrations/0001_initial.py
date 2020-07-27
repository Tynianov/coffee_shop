# Generated by Django 2.2.14 on 2020-07-27 22:13

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='Designate, if object is active', verbose_name='Is active?')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Post content')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='post/images', verbose_name='Post image')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='post.Post')),
            ],
            options={
                'verbose_name': 'Post image',
                'verbose_name_plural': 'Post images',
            },
        ),
    ]
