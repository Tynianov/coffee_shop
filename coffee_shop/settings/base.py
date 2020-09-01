"""
Django settings for coffee_shop project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from .local import *
from django.utils.translation import ugettext_lazy as _
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's3qj8p8)8jjc#(0t*efxzb@*d-4piqq5!x66w5b+s60#d^4g)9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'ckeditor',
    'drf_yasg',
    'phonenumber_field',
    'fcm_django',

    'voucher',
    'menu',
    'user',
    'qr_code',
    'config',
    'post',
    'api',
    'logs',
    'sms'
]
SITE_ID = 1
# PROTOCOL = 'https'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'coffee_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'coffee_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'coffee_shop',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#             # 'init_command': 'SET storage_engine=InnoDB; SET sql_mode="STRICT_TRANS_TABLES"',
#             'charset': 'utf8mb4',
#             'use_unicode': True,
#         },
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

LOCALE_PATHS = ('locale', BASE_DIR)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

ADMIN_URL = 'admin'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTH_USER_MODEL = 'user.User'

DATETIME_FORMAT = "d/m/Y H:i:s"

DATE_FORMAT = "d/m/Y"

DATETIME_OUTPUT_FORMAT = "%d/%m/%Y %H:%M"

DATE_OUTPUT_FORMAT = "%d/%m/%Y"

DATE_INPUT_FORMATS = [
    '%d/%m/%Y'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.TemplateHTMLRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        # 'extras.dashboard.throttles.EventRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '90000/day',
        'user': '90000/day',
        'event': '1000/min',
    },
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',
    # 'EXCEPTION_HANDLER': 'knpay.error_handler.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    # 'VIEW_DESCRIPTION_FUNCTION': 'rest_framework_swagger.views.get_restructuredtext',
    # 'PAGE_SIZE': 20,
    # 'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'base.negotiation.BrowserOrAPIContentNegotiation'
    'DATETIME_FORMAT': DATETIME_OUTPUT_FORMAT,
    'DATE_FORMAT': DATE_OUTPUT_FORMAT,
    'DATETIME_INPUT_FORMATS': ['%d/%m/%Y %H:%M'],
    "DATE_INPUT_FORMATS": DATE_INPUT_FORMATS + ['iso-8601'],
}

ACCOUNT_AUTHENTICATION_METHOD = 'phone_number'
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = False

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'user.serializers.UpdateUserDetailsSerializer',
    'LOGIN_SERIALIZER': "user.serializers.CustomLoginSerializer"
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': "user.serializers.CustomRegistrationSerializer"
}

SMS_CODE_DURATION = 10  # in minutes

# sentry_sdk.init(
#     dsn=SENTRY_DSN,
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=1.0,
#
#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )
