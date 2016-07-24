# encoding:utf8
""" By Daath """

from django.db import models
from mongoengine import *
from mongoengine.base import BaseDocument
from application.exception import prefURL
import json

# Create your models here.

defaultAvatar = prefURL['ImageURL'] + 'avatar/defaultUserImage.png'

# app用户表
class User(Document):
    account = StringField(required=True)
    password = StringField(required=True)
    avatar = StringField(default=defaultAvatar)
    nickname = StringField(max_length=50, default="")
    realName = StringField(max_length=50, default="")
    description = StringField(max_length=150, default="")
    phone = StringField(max_length=11, default="")
    # ['user', 'applyGuide', 'guide']    用户, 导游申请， 导游
    status = StringField(default="user")
    location = PointField(default=[0.0000000000, 0.0000000000])
    token = StringField(default="")
    channelId = StringField(default="")

    def to_json(self):
        user_json = BaseDocument.to_json(self)
        user_dict = json.loads(user_json)
        user_dict['_id'] = user_dict['_id']['$oid']
        user_dict['location'] = user_dict['location']['coordinates']
        user_dict.pop('password')
        return json.dumps({"result": user_dict})


# 管理后台管理员表
class AdminUser(Document):
    account = StringField(required=True)
    password = StringField(required=True)
    avatar = StringField(default=defaultAvatar)
    nickname = StringField(max_length=50, default="")
    realName = StringField(max_length=50, required=True)
    description = StringField(max_length=150, default="")
    phone = StringField(max_length=11, default="")
    # ['applyAdmin', 'admin']    管理员申请， 管理员
    status = StringField(default="applyAdmin")
    location = PointField(default=[0.0000000000, 0.0000000000])
    token = StringField(default="")
    channelId = StringField(default="")

    def to_json(self):
        admin_user_json = BaseDocument.to_json(self)
        admin_user_dict = json.loads(admin_user_json)
        admin_user_dict['_id'] = admin_user_dict['_id']['$oid']
        admin_user_dict['location'] = admin_user_dict['location']['coordinates']
        admin_user_dict.pop('password')
        return json.dumps({"result": admin_user_dict})


"""
    通过Django的ORM来存储图片，然后在将图片地址给予用户表的头像字段
"""
class UserAvatar(models.Model):
    user_avatar = models.ImageField(upload_to="avatar")


class ImageTest(models.Model):
    image_avatar = models.ImageField(upload_to="photo")


