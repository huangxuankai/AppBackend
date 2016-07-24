# encoding:utf8
""" By Daath """

from django.http import *
from mongoengine import Q

from .models import Scene
import json
from application.function import id_replace, more_replace
from application.exception import resultMsg

# Create your views here.


"""
    /scene/lists/  获得景区列表
    Method: POST
    Parameter: |  skip limit latitude longitude
    JSON: {
        "result": [
            {
                "province": "湖南省",
                "city": "张家界",
                "name": "张家界",
                "image": "http://photocdn.sohu.com/20150720/mp23435940_1437361439743_3.jpeg",
                "_id": "56de86d77a74e763f3b29186",
                "description": "这是一个很好的地方"
            },
            ...
        ]
    }
"""
def scene_lists(request):
    if request.method == "POST":
        try:
            skip = int(request.POST.get('skip', 0))
        except (TypeError, ValueError) as e:
            skip = 0
        try:
            limit = int(request.POST.get('limit', 5))
        except (TypeError, ValueError) as e:
            limit = 5
        # 查看是否有坐标参数
        try:
            latitude = float(request.POST.get('latitude', None))
            longitude = float(request.POST.get('longitude', None))
        except:
            return JsonResponse(resultMsg['CoordinatesError'])
        coordinates = [longitude, latitude]     # 做成坐标组
        lists = Scene.objects(status='online', location__near=coordinates, location__max_distance=50000).all()[skip: limit]
        lists = json.loads(lists.to_json())
        map(more_replace, lists)
        return JsonResponse({"result": lists})
    raise Http404


"""
    /scene/search/  搜索景区
    Method: POST
    Parameter: |  skip limit latitude longitude
    JSON: {
        "result": [
            {
                "province": "湖南省",
                "city": "张家界",
                "name": "张家界",
                "image": "http://photocdn.sohu.com/20150720/mp23435940_1437361439743_3.jpeg",
                "_id": "56de86d77a74e763f3b29186",
                "description": "这是一个很好的地方"
            },
            ...
        ]
    }
"""
def scene_search(request):
    if request.method == "POST":
        try:
            skip = int(request.POST.get('skip', 0))
        except TypeError:
            skip = 0
        except ValueError:
            skip = 0
        try:
            limit = int(request.POST.get('limit', 5))
        except TypeError:
            limit = 5
        except ValueError:
            limit = 5
        # # 查看是否有坐标参数
        # try:
        #     latitude = float(request.POST.get('latitude', None))
        #     longitude = float(request.POST.get('longitude', None))
        # except:
        #     return JsonResponse(resultMsg['CoordinatesError'])
        # coordinates = [longitude, latitude]     # 做成坐标组

        # 判断搜索内容
        content = request.POST.get('searchContent', None)
        if not content:
            return JsonResponse(resultMsg['NeedParameter'])
        lists = Scene.objects(
            (Q(name={"$regex": content}) |
            Q(city={"$regex": content}) |
            Q(province={"$regex": content})),
            status='online'
            # location__near=coordinates, location__max_distance=50000
        ).all()[skip: limit]
        lists = json.loads(lists.to_json())
        map(more_replace, lists)
        return JsonResponse({"result": lists})
    raise Http404


def test(request):
    raise Http404
