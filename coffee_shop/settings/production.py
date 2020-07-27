from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coffee_shop',
        'USER': 'root',
        'PASSWORD': '1',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=InnoDB',
            'charset': 'utf8',
            'use_unicode': True,
        },
    }
}