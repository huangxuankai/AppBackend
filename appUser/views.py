# encoding:utf8
""" By Daath """

from django.contrib import auth
from django.core.files.base import ContentFile
from mongoengine import document
from django.http import *
from models import User, ImageTest, UserAvatar
import json
from application.exception import resultMsg, prefURL
from application.function import id_replace, login_auth, produce_image_name, process_token, push_nearly_scene
from base64 import b64decode

# Create your views here.

"""
    api/user/signCheck/  app用户登录检查
    Method: POST
    JSON: {
        'error': False,
        'msgCode': 2,
        'msg': "sign check successful"
    }
"""
def sign_check(request):
    if request.method == "POST":
        is_exist = request.session.get('currentUser', None)
        if is_exist:
            return JsonResponse(resultMsg['SignCheckSuccessful'])
        return JsonResponse(resultMsg['NeedLogin'])
    raise Http404


"""
    api/user/signUp/  用户注册
    Method: POST
    Parameter: |  account password
    JSON: {
        "msg": "exist user",
        "msgCode": 1001,
        "error": true
    }
"""
def sign_up(request):
    if request.method == "POST":
        account = request.POST.get('account', '')
        password = request.POST.get('password', '')
        if not account or not password:
            return JsonResponse(resultMsg['NeedParameter'])
        is_exist = User.objects(account=account).filter().count()
        if is_exist:
            return JsonResponse(resultMsg['ExistUser'])
        user = User()
        user.account = account
        user.password = password
        user.save()
        kw = {
            '_id': str(user.id),
            'nickname': user.nickname,
            'avatar': user.avatar,
            'token': user.token
        }
        process_token(**kw)
        return JsonResponse(resultMsg['SignUpSuccess'])
    raise Http404


"""
    api/user/signIn/  用户登录
    Method: POST
    Parameter: |  account password
    JSON: {
        "result": {
            "status": "guide",
            "account": "Daath",
            "_id": "56dc4a407a74e720e5d3ce24",
            "realName": "李四",
            "location": {
                "type": "Point",
                "coordinates": [
                    113.363911,
                    23.140113
                ]
            },
            "phone": "1364",
            "avatar": "http://img4q.duitang.com/uploads/item/201406/30/20140630190350_HLd4L.jpeg",
            "nickname": "好",
            "description": "真诚待人，希望做更好"
        }
    }
"""
def sign_in(request):
    if request.method == "POST":
        account = request.POST.get('account', None)
        password = request.POST.get('password', None)
        if not account or not password:
            return JsonResponse(resultMsg['NeedParameter'])
        try:
            user = User.objects(account=account).get()
        except User.DoesNotExist:
            return JsonResponse(resultMsg['NotExistUser'])
        if user.password == password:
            request.session['currentUser'] = {"_id": str(user.id)}
            kw = {
                '_id': str(user.id),
                'nickname': user.nickname,
                'avatar': user.avatar,
                'token': user.token
            }
            process_token(**kw)
            user.reload()
            return HttpResponse(user.to_json())
        return JsonResponse(resultMsg['ErrorPassword'])
    raise Http404


"""
    api/user/signOut/  用户退出
    Method: POST
    JSON: {
        "msg": "sign out",
        "msgCode": 1,
        "error": False
    }
"""
def sign_out(request):
    try:
        del request.session['currentUser']
    except KeyError:
        pass
    return JsonResponse(resultMsg['SignOut'])


"""
    api/user/update/  更新用户资料
    Method: POST
    Parameter: |  nickname realName description phone
    JSON: {
        "result": {
            "status": "guide",
            "account": "Daath",
            "_id": "56dc4a407a74e720e5d3ce24",
            "realName": "李四",
            "location": {
                "type": "Point",
                "coordinates": [
                    113.363911,
                    23.140113
                ]
            },
            "phone": "1364",
            "avatar": "http://img4q.duitang.com/uploads/item/201406/30/20140630190350_HLd4L.jpeg",
            "nickname": "赵日天",
            "description": "真诚待人，希望做更好"
        }
    }
"""
@login_auth
def update(request):
    if request.method == "POST":
        nickname = request.POST.get('nickname', None)
        real_name = request.POST.get('realName', None)
        description = request.POST.get('description', None)
        phone = request.POST.get('phone', None)
        update_dict = dict()
        if nickname:
            update_dict['nickname'] = nickname
        if real_name:
            update_dict['realName'] = real_name
        if description:
            update_dict['description'] = description
        if phone:
            update_dict['phone'] = phone
        user = User.objects(id=request.session['currentUser']['_id']).get()
        if update_dict:
            user.update(**update_dict)
            user.reload()
            if nickname:
                kw = {
                    '_id': str(user.id),
                    'nickname': user.nickname,
                    'avatar': user.avatar,
                    'token': user.token
                }
                process_token(**kw)
        return HttpResponse(user.to_json())
    raise Http404


"""
    api/user/updateLocation/  用户定位坐标更新
    Method: POST
    Parameter: |  latitude longitude
    JSON: { 当前用户的信息 }
"""
@login_auth
def update_location(request):
    if request.method == "POST":
        try:
            latitude = float(request.POST.get('latitude', None))
            longitude = float(request.POST.get('longitude', None))
        except:
            return JsonResponse({"message": "坐标有错"})
        coordinates = [longitude, latitude]
        user = User.objects(id=request.session['currentUser']['_id']).get()
        user.update(location=coordinates)
        user.reload()
        print coordinates
        kw = {
            'channelId': user.channelId,
            'coordinates': [longitude, latitude]
        }
        push_nearly_scene(**kw)
        return HttpResponse(user.to_json())
    raise Http404


"""
    api/user/modifyPassword/  修改用户密码
    Method: POST
    Parameter: |  oldPassword newPassword
    JSON: {
        "result": {
            "status": "guide",
            "account": "Daath",
            "_id": "56dc4a407a74e720e5d3ce24",
            "realName": "李四",
            "location": {
                "type": "Point",
                "coordinates": [
                    113.363911,
                    23.140113
                ]
            },
            "phone": "1364",
            "avatar": "http://img4q.duitang.com/uploads/item/201406/30/20140630190350_HLd4L.jpeg",
            "nickname": "赵日天",
            "description": "真诚待人，希望做更好"
        }
    }
"""
@login_auth
def modify_password(request):
    if request.method == "POST":
        old_password = request.POST.get('oldPassword', None)
        new_password = request.POST.get('newPassword', None)
        if not old_password or not new_password:
            return JsonResponse(resultMsg['NeedParameter'])
        try:
            update_user = User.objects(id=request.session['currentUser']['_id'], password=old_password).get()
        except User.DoesNotExist:
            return JsonResponse(resultMsg['ErrorPassword'])
        update_user.update(password=new_password)
        update_user.reload()
        return HttpResponse(update_user.to_json())
    raise Http404


"""
    api/user/applyGuide/  申请导游
    Method: POST
    JSON: { 当前用户的信息 }
"""
@login_auth
def apply_guide(request):
    if request.method == "POST":
        user = User.objects(id=request.session['currentUser']['_id']).get()
        user.update(status="applyGuide")
        user.reload()
        return HttpResponse(user.to_json())
    raise Http404


"""
    api/user/getGuideLists/ 获得导游列表
    Method: POST
    Parameter: |  skip limit latitude longitude
    Json: {
        "result": [
            {
                "_id": "56de77c3e82017c1a0556aff",
                "realName": "banana",
                "avatar": "http://b.picphotos.baidu.com/album/s%3D1100%3Bq%3D90/sign=63fc9698e7fe9925cf0c6d51049865ae/060828381f30e924e14c126c4b086e061c95f787.jpg",
                "description": "带好您的行李，走遍中国，尽力为每一个游客细心周到的解说景区"
            }
        ]
    }
"""
def get_guide_lists(request):
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
        print coordinates
        guides = User.objects(
            status='guide',
            location__near=coordinates,
            location__max_distance=10000
        ).only('id', 'realName', 'avatar', 'description').all()[skip: limit]
        guides = json.loads(guides.to_json())
        print guides
        map(id_replace, guides)
        return JsonResponse({"result": guides})
    raise Http404


"""
    api/user/getVisitorLists/ 获得附近游客列表
    Method: POST
    Parameter: |  skip limit latitude longitude
    Json: {
        "result": [
            {
                "_id": "56de77c3e82017c1a0556aff",
                "realName": "banana",
                "avatar": "http://b.picphotos.baidu.com/album/s%3D1100%3Bq%3D90/sign=63fc9698e7fe9925cf0c6d51049865ae/060828381f30e924e14c126c4b086e061c95f787.jpg",
                "description": "带好您的行李，走遍中国，尽力为每一个游客细心周到的解说景区"
            }
        ]
    }
"""
def get_visitor_lists(request):
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
        print coordinates
        visitors = User.objects(
            id__ne=request.session['currentUser']['_id'],
            status__in=['user', 'applyGuide'],
            location__near=coordinates,
            location__max_distance=10000
        ).only('id', 'realName', 'avatar', 'description').all()[skip: limit]
        visitors = json.loads(visitors.to_json())
        map(id_replace, visitors)
        return JsonResponse({"result": visitors})
    raise Http404


"""
    api/user/avatarUpload/  头像上传
    Method: POST
    Parameter: |  file 是base64字节流
    JSON: { 当前用户的信息}
"""
@login_auth
def avatar_upload(request):
    if request.method == "POST":
        image_stream = request.POST.get('file', None)
        image = ContentFile(b64decode(image_stream))
        avatar = UserAvatar()
        avatar.user_avatar.save(produce_image_name() + '.jpg', image)
        current_user = User.objects(id=request.session['currentUser']['_id']).get()
        image_url = prefURL['ImageURL'] + avatar.user_avatar.__str__()
        current_user.update(avatar=image_url)
        current_user.reload()
        kw = {
            '_id': str(current_user.id),
            'nickname': current_user.nickname,
            'avatar': current_user.avatar,
            'token': current_user.token
        }
        process_token(**kw)
        return HttpResponse(current_user.to_json())
    raise Http404


"""
    api/user/tokenReload/  token过期，重新获取token
    Method: POST
    JSON: { 当前游客的部分信息}
"""
@login_auth
def token_reload(request):
    if request.method == "POST":
        current_user = User.objects(id=request.session['currentUser']['_id']).get()
        kw = {
            '_id': str(current_user.id),
            'nickname': current_user.nickname,
            'avatar': current_user.avatar,
            'token': ''
        }
        process_token(**kw)
        current_user.reload()
        print current_user.token
        return HttpResponse(current_user.to_json())
    raise Http404


"""
    api/user/saveChannelId/  保存百度云推送的channelId
    Method: POST
    Parameter: |  channelId
    JSON: {
        'error': False,
        'msgCode': 3,
        'msg': "save channelId successful"
    }
"""
@login_auth
def save_channel_id(request):
    if request.method == "POST":
        channel_id = request.POST.get('channelId', None)
        if not channel_id:
            return JsonResponse(resultMsg['NeedParameter'])
        current_user = User.objects(id=request.session['currentUser']['_id']).get()
        current_user.update(channelId=channel_id)
        return JsonResponse(resultMsg['SaveChannelId'])
    raise Http404


"""
    api/user/getVisitorInfo/  获取游客用户信息(这个暂时没用到)
    Method: POST
    Parameter: |  id
    JSON: { 当前游客的部分信息}
"""
@login_auth
def get_visitor_info(request):
    if request.method == "POST":
        visitor_id = request.POST.get('id', None)
        if not visitor_id:
            return JsonResponse(resultMsg['NeedParameter'])
        visitor = User.objects(id=visitor_id).only('id', 'realName', 'nickname', 'avatar').get()
        result = {
            '_id': str(visitor.id),
            'realName': visitor.realName,
            'nickname': visitor.nickname,
            'avatar': visitor.avatar
        }
        return JsonResponse({'result': result})
    raise Http404


def test(request):
    # if request.session['user']:
    #     print request.session['user']
    #     return JsonResponse({"aaa": 123})
    # userTest = User.objects().all()
    # xx = json.loads(userTest.to_json())
    # return JsonResponse({"result": xx})
    # return HttpResponse(userTest.to_json())
    # xx = request.session['xx']
    # x = json.dumps(xx)
    # del request.session['xx']
    return JsonResponse({"ss": 11}, status=201)
    # list1 = [
    #     [116.4135540000, 39.9110130000],
    #     [112.4717700000, 23.0529840000],
    #     [112.9453330000, 28.2339710000],
    #     [113.3351650000, 23.1401800000],
    #
    # ]
    # user = User.objects(location__near=list1[3], location__max_distance=10000)
    # if not user:
    #     print 'xx'
    # return HttpResponse(user.to_json())


"""
    上传图片测试
"""
def image_test(request):
    if request.method == "GET":
        print request.method
        return JsonResponse({"result": 555})
    if request.method == "POST":
        print 123
        xxs = request.POST.get('file', None)
        # print xxs
        # print type(xxs)
        image_data = ContentFile(b64decode(xxs))
        # file = ContentFile(xxs)
        # print request.FILES
        # print request.FILES['file'].__dict__
        # print bytes(request.FILES['file'])
        # print type(request.FILES['file'])
        x = ImageTest()
        # file = ContentFile(request.FILES['file'].read())
        # # x.save()
        x.image_avatar.save("test.jpg", image_data)
        return JsonResponse({"result": 555})



