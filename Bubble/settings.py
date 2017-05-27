#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from __future__ import unicode_literals
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'

SECRET_KEY = 'zph8*z8s%8jva0k*6y7i*2i&2@kv$3%0^m9ahntdxr@+_je$om'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bubble',
        'USER': 'root',
        'PASSWORD': 'BubbleLocalHost',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}


PAYMENT = {
    'aggregator': 'free-kassa',
    'publicKey': '51131',
    'secretKey': 'dbt44xm8',
    'secretKey2': 'hb63vjv4',    # only for free-kassa
    'currency': 'RUB'
}


BUBBLE = {
    'siteName': 'Bubble',
    'serverIp': 'BUBBLE.LOCALHOST',
    'description': 'Donation system written with Django',
    'descriptionOfPurchase': 'Покупка {item} для {account} на {siteName}',  # {account}, {item}, {siteName}
    'messageOfPending': 'Ожидается выполнение платежа!',
    'messageOfSuccess': 'Поздравляем с покупкой!',
    'messageOfFail': 'Что-то пошло не так. Попробуйте ещё раз!'
}

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]'
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'basic'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'Bubble.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + 'templates',
            BASE_DIR + 'basic/templates'
        ],
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


WSGI_APPLICATION = 'Bubble.wsgi.application'


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


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    BASE_DIR + 'static/',
]
