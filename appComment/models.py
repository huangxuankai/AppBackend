# encoding:utf8
""" By Daath """

from django.db import models
from mongoengine import *
from mongoengine.base import BaseDocument
import json
import datetime
import time
# Create your models here.


class SceneComment(Document):
    sceneId = StringField(required=True)
    userId = StringField(required=True)
    content = StringField(default=None)
    commentTime = DateTimeField(default=datetime.datetime.now())

    def to_json(self):
        comment_json = BaseDocument.to_json(self)
        comment_dict = json.loads(comment_json)
        comment_dict['_id'] = comment_dict['_id']['$oid']
        return json.dumps({"result": comment_dict})


class GuideComment(Document):
    guideId = StringField(required=True)
    userId = StringField(required=True)
    content = StringField(default=None)
    commentTime = DateTimeField(default=datetime.datetime.now())

    def to_json(self):
        comment_json = BaseDocument.to_json(self)
        comment_dict = json.loads(comment_json)
        return json.dumps({"result": comment_dict})