# encoding:utf8
""" By Daath """

from django.db import models
from mongoengine import *
from mongoengine.base import BaseDocument
import json

# Create your models here.


class Scene(Document):
    name = StringField(max_length=150)
    image = StringField(default="")
    description = StringField(default="")
    city = StringField(default="")
    province = StringField(default="")
    status = StringField(default="offline")      # [online, offline]  上线 下线
    location = PointField(default=[0.0000000000, 0.0000000000])     # [经度Longitude, 纬度Latitude]

    def to_json(self):
        scene_json = BaseDocument.to_json(self)
        scene_dict = json.loads(scene_json)
        return json.dumps({"result": scene_dict})

    def data_clean(self):
        scene_json = BaseDocument.to_json(self)
        scene_dict = json.loads(scene_json)
        scene_dict['id'] = scene_dict['_id']['$oid']
        scene_dict['longitude'] = scene_dict['location']['coordinates'][0]
        scene_dict['latitude'] = scene_dict['location']['coordinates'][1]
        scene_dict.pop('_id')
        scene_dict.pop('location')
        return scene_dict


class SceneImage(models.Model):
    image = models.ImageField(upload_to="sceneImage")
