# encoding:utf8
""" By Daath """

from django.http import *
from django.shortcuts import *
from .exception import resultMsg
from module.rongSDK.rong import ApiClient
from appUser.models import User
from appScene.models import Scene
from module.baiduPushSDK.Channel import *
import random
import time
import json
""" 自定义的功能函数 """


def id_replace(l):
    l['_id'] = l['_id']['$oid']


def more_replace(l):
    l['_id'] = l['_id']['$oid']
    l['location'] = l['location']['coordinates']


def web_id_replace(l):
    l['id'] = l['_id']['$oid']
    l.pop('_id')


def login_auth(function):
    def wrapper(request):
        if request.session.get('currentUser', None):
            return function(request)
        return JsonResponse(resultMsg['NeedLogin'])
    return wrapper


def admin_login_auth(function):
    def wrapper(request):
        if request.session.get('currentAdmin', None):
            return function(request)
        return render(request, 'signIn.html', {'error': '登录已失效，请重新登录'})
    return wrapper


def produce_image_name(length=16):
    name = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    for i in xrange(length):
        name += random.choice(chars)
    # 加上时间戳　
    name += str(int(time.time()))
    return name


def process_token(**kw):
    api = ApiClient()
    print kw
    if kw['token']:
        params = {
            'user_id': kw['_id'],
            'name': kw['nickname'],
            'portrait_uri': kw['avatar']
        }
        response = api.user_refresh(**params)
        if response['code'] == 200:
            return
    else:
        params = {
            'user_id': kw['_id'],
            'name': kw['nickname'],
            'portrait_uri': kw['avatar']
        }
        response = api.user_get_token(**params)
        if response['code'] == 200:
            user = User.objects(id=kw['_id']).get()
            user.update(token=response['token'])
            return
    print response
    return


def push_nearly_scene(**kw):
    channel_id = kw['channelId'].encode('utf-8')
    coordinates = kw['coordinates']
    lists = Scene.objects(status='online', location__near=coordinates, location__max_distance=5000).all()[:1]
    lists = json.loads(lists.to_json())
    print channel_id, coordinates
    push_msg = {
        'title': '系统通知',
        'description': '距离您5000米最近的景区是：' + lists[0]['name'].encode('utf-8'),
        'custom_content': {
            'content': 'value1',
        },
    }
    opts = {'msg_type':1, 'expires':300}
    c = Channel()
    c.setApiKey('ljYNLqCZdMzY6DsyCyzXEgdss8YmtOFL')
    c.setSecretKey('8sGfm4SSDL1KFuLaPyrdHqNs9Qp9nPkG')
    try:
        ret = c.pushMsgToSingleDevice(channel_id, json.dumps(push_msg), opts)
        print 'ret: ',
        print ret
        print c.getRequestId()
    except ChannelException as e:
        print '[code]',
        print e.getLastErrorCode()
        print '[msg]',
        print e.getLastErrorMsg()
        print '[request id]',
        print c.getRequestId()
