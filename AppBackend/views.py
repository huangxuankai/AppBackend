# encoding:utf8
""" By Daath """

from appUser.models import User
from django.http import *
import json


def home(request):
    return HttpResponseRedirect('/admin/user/adminCenter/')


"""    暂时没用    """
def visitor_lists(request):
    if not request.session['user']:
        return JsonResponse({"message": "need login"})
    if request.method == "POST":
        point = [
            [116.4135540000, 39.9110130000],
            [112.4717700000, 23.0529840000],
            [112.9453330000, 28.2339710000],
            [113.3351650000, 23.1401800000],
        ]
        lists = User.objects(status="user", location__near=point[3], location__max_distance=10000)
        lists = json.loads(lists.to_json())
        return JsonResponse({"result": lists})
    raise Http404


"""    暂时没用    """
def guide_lists(request):
    if not request.session['user']:
        return JsonResponse({"message": "need login"})
    if request.method == "POST":
        point = [
            [116.4135540000, 39.9110130000],
            [112.4717700000, 23.0529840000],
            [112.9453330000, 28.2339710000],
            [113.3351650000, 23.1401800000],
        ]
        lists = User.objects(status="guide", location__near=point[3], location__max_distance=10000)
        lists = json.loads(lists.to_json())
        return JsonResponse({"result": lists})
    raise Http404

