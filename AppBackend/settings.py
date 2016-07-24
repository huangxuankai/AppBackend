# encoding:utf8
"""
Django settings for AppBackend project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
from mongoengine import connect

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2a)rhd0f1aqg&dwf@)ar4z_e70o5hbvzja&rpsmkz&p@%3ez)f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appUser',
    'appScene',
    'appComment',
    'application',
    'module'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

# APPEND_SLASH = False
ROOT_URLCONF = 'AppBackend.urls'

WSGI_APPLICATION = 'AppBackend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
    }
}

# NoSql Database Mongodb connect
connect('travelDB', username='root', password='root', authentication_source='admin')

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# STATIC_ROOT = '/home/daath/PycharmProjects/AppBackend/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

# MEDIA_ROOT = '/home/daath/PycharmProjects/AppBackend/static/media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'templates'),    # static路径下的html模板会从template目录获取
    ("media", os.path.join(STATIC_ROOT, 'media')),
    ("bootstrap", os.path.join(STATIC_ROOT, 'bootstrap')),
    ("jquery", os.path.join(STATIC_ROOT, 'jquery')),
    ("css", os.path.join(STATIC_ROOT, 'css')),
    ("js", os.path.join(STATIC_ROOT, 'js')),
)

# 融云IM 测试环境
app_key = "6tnym1brnoca7"
app_secret = "fHF6HyP2BsswbU"
os.environ.setdefault('rongcloud_app_key', app_key)
os.environ.setdefault('rongcloud_app_secret', app_secret)

# 融云IM 正式环境
# app_key = ""
# app_secret = ""
# os.environ.setdefault('rongcloud_app_key', app_key)
# os.environ.setdefault('rongcloud_app_secret', app_secret)

logging.basicConfig(level=logging.INFO)
