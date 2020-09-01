DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'host',
        'PORT': '3306',
        'OPTIONS': {
            # 'init_command': 'SET storage_engine=InnoDB; SET sql_mode="STRICT_TRANS_TABLES"',
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False


PROTOCOL = 'http'

SECRET_KEY = 'your secret key'

TWILIO_SID = 'twilio sid'
TWILIO_AUTH_TOKEN = 'twilio key'
TWILIO_PHONE_NUMBER = 'twilio phone number'
SENTRY_DSN = 'sentry dsn'
