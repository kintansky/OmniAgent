"""
Django settings for omni project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(n)6f(v^7ty62&fcr9(=1#awr9^2jb&#1tdf6jk!+*0i#a)(*j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# django连接mysql 参考官方文档 https://dev.mysql.com/doc/connector-python/en/connector-python-django-backend.html
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': 'mysql.connector.django',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'omni_agent',
        'USER': 'root',
        'PASSWORD': 'hlw2019!@#$',
        'HOST': '127.0.0.1',
        'PORT': '9003',
        'OPTIONS': {
            'autocommit': True,
        },
    },
    # networkresource使用的是cmdb数据库，migrate的时候需要指定--database=...
    'cmdb': {
        # 'ENGINE': 'mysql.connector.django',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cmdb',
        'USER': 'root',
        'PASSWORD': 'hlw2019!@#$',
        'HOST': '127.0.0.1',
        'PORT': '9003',
        'OPTIONS': {
            'autocommit': True,
        },
    }
}

