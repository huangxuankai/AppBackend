# encoding:utf8
""" By Daath """

import os

from django.test import TestCase

# Create your tests here.

# from models import User
from mongoengine import connect
import json
import random
import time
# x = ''
# if not x:
#     print 12
# else:
#     print 32

# connect('travelDB', username='root', password='root', authentication_source='admin')
# # is_exist = User.objects.get(account="D")
# try:
#     is_exist = User.objects(account="Daath").filter()
# except User.DoesNotExist:
#     is_exist = None
#
# print is_exist
# if not is_exist:
#     print 11

#
# def random_str():
#     str1 = ''
#     chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
#     for i in xrange(22):
#         str1 += random.choice(chars)
#
#     str1 += str(int(time.time()))
#     return str1
#
# xx = random_str()
# print len(xx)
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
# STATICFILES_DIRS = (
#     ("media", os.path.join(STATIC_ROOT, 'media')),
# )
#
# DATABASE_NAME = os.path.join(BASE_DIR, 'db/db.sqlite3')
# print DATABASE_NAME
# # print BASE_DIR
# # print MEDIA_ROOT
# # print STATIC_ROOT
# # print STATICFILES_DIRS
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         # 'NAME': '/home/daath/PycharmProjects/AppBackend/db/db.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
#     }
# }
# print DATABASES

import os
import json
import unittest
import logging

from module.rongSDK.rong import ApiClient

app_key = "6tnym1brnoca7"
app_secret = "fHF6HyP2BsswbU"

# 您应该将key 和 secret 保存在服务器的环境变量中
os.environ.setdefault('rongcloud_app_key', app_key)
os.environ.setdefault('rongcloud_app_secret', app_secret)

logging.basicConfig(level=logging.INFO)

api = ApiClient()
user = {
    'user_id': '56dc4a407a74e720e5d3ce24',
    'name': 'Daath',
    'portrait_uri': 'http://192.168.0.106:8003/static/media/avatar/NMcDvQAkNZj4smxn1459863254.jpg'
}
Token = api.user_get_token(**user)

print Token



