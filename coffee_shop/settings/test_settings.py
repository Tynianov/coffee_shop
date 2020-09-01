DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coffee_shop_test_db',  # you need to create database `test_db` or db user must have permissions to do that
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            # 'init_command': 'SET storage_engine=InnoDB; SET sql_mode="STRICT_TRANS_TABLES"',
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    },
}

SECRET_KEY = '(0dasd' * 5
