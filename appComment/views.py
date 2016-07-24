# encoding:utf8
""" By Daath """
import datetime
from django.http import *
from .models import SceneComment, GuideComment
from appScene.models import Scene
from appUser.models import User
import json
from application.exception import resultMsg
from application.function import login_auth


# Create your views here.


"""
    /comment/commentScene/  评论景区
    Method: POST
    Parameter: |  id content
    JSON = {
        "result": {
            "sceneId": "56de885c7a74e76673e2e7b7",
            "content": "这是个好景区",
            "_id": "56ff70d27a74e760897c8183",
            "userId": "56dc4a407a74e720e5d3ce24",
            "commentTime": {
                "$date": 1459581122315
            }
        }
    }
"""
@login_auth
def comment_scene(request):
    if request.method == "POST":
        scene_id = request.POST.get('id', None)
        content = request.POST.get('content', None)
        if not scene_id or not content:
            return JsonResponse(resultMsg['NeedParameter'])
        comment = SceneComment()
        comment.sceneId = scene_id
        comment.userId = request.session['currentUser']['_id']
        comment.content = content
        comment.save()
        comment.reload()
        return HttpResponse(comment.to_json())
    raise Http404


"""
    /comment/commentGuide/  评论导游
    Method: POST
    Parameter: |  id content
    JSON = {
        "result": {
            "guideId": "56de77c3e82017c1a0556aff",
            "content": "这是个好导游",
            "_id": {
                "$oid": "56ff71627a74e765eb541f81"
            },
            "userId": "56dc4a407a74e720e5d3ce24",
            "commentTime": {
                "$date": 1459581282233
            }
        }
    }
"""
@login_auth
def comment_guide(request):
    if request.method == "POST":
        guide_id = request.POST.get('id', None)
        content = request.POST.get('content', None)
        if not guide_id or not content:
            return JsonResponse(resultMsg['NeedParameter'])
        comment = GuideComment()
        comment.guideId = guide_id
        comment.userId = request.session['currentUser']['_id']
        comment.content = content
        comment.save()
        comment.reload()
        return HttpResponse(comment.to_json())
    raise Http404


"""
    /comment/getSceneComment/ 获得景区评论
    Method: POST
    Parameter: |  id
    JSON = {
        "haveComment": true,
        "result": [
            {
                "content": "黄埔古港是个好地方",
                "userId": "56dc4a407a74e720e5d3ce24",
                "sceneId": "56de885c7a74e76673e2e7b7",
                "userInfo": {
                    "_id": "56dc4a407a74e720e5d3ce24",
                    "nickname": "好",
                    "avatar": "http://img4q.duitang.com/uploads/item/201406/30/20140630190350_HLd4L.jpeg"
                },
                "commentTime": {
                    "$date": 1459580864691
                },
                "_id": "56ff6fe27a74e75d7f2b0a4d"
            }
        ]
    }
"""
def get_scene_comment(request):
    if request.method == "POST":
        scene_id = request.POST.get("id", None)
        if not scene_id:
            return JsonResponse(resultMsg['NeedParameter'])
        comments = SceneComment.objects(sceneId=scene_id).all()
        comments = json.loads(comments.to_json())
        user_ids = list(set(map(lambda l: l['userId'], comments)))
        users = User.objects(id__in=user_ids).only("id", "nickname", "avatar").all()
        users = json.loads(users.to_json())
        for comment in comments:
            comment['_id'] = comment['_id']['$oid']
            for user in users:
                if user['_id']['$oid'] == comment['userId']:
                    comment['userInfo'] = {
                        '_id': user['_id']['$oid'],
                        'nickname': user['nickname'],
                        'avatar': user['avatar'],
                    }
        print request.COOKIES
        response = {
            'result': comments,
            'haveComment': False
        }
        if request.session['currentUser']['_id'] in user_ids:
            response['haveComment'] = True
        return JsonResponse(response)
    raise Http404


"""
    /comment/getGuideComment/  获得导游评论表
    Method: POST
    Parameter: |  id
    JSON: {
        "haveComment": true,
        "result": [
            {
                "guideId": "56dc4a407a74e720e5d3ce24",
                "userId": "56dd1f6e80980daee16a8dc5",
                "content": "Tiger是个不错的导游",
                "userInfo": {
                    "_id": "56dd1f6e80980daee16a8dc5",
                    "nickname": "hani",
                    "avatar": "http://b.picphotos.baidu.com/album/s%3D1100%3Bq%3D90/sign=63fc9698e7fe9925cf0c6d51049865ae/060828381f30e924e14c126c4b086e061c95f787.jpg"
                },
                "commentTime": {
                    "$date": 1459427991298
                },
                "_id": "56fd18132f3f565529a0e1cd"
            },
            {
                "guideId": "56dc4a407a74e720e5d3ce24",
                "userId": "56dc4a407a74e720e5d3ce24",
                "content": "来一波评论自己的",
                "userInfo": {
                    "_id": "56dc4a407a74e720e5d3ce24",
                    "nickname": "好",
                    "avatar": "http://img4q.duitang.com/uploads/item/201406/30/20140630190350_HLd4L.jpeg"
                },
                "commentTime": {
                    "$date": 1459580148277
                },
                "_id": "56ff6cf47a74e74e9bb3b069"
            }
        ]
    }

"""
def get_guide_comment(request):
    if request.method == "POST":
        guide_id = request.POST.get("id", None)
        if not guide_id:
            return JsonResponse(resultMsg['NeedParameter'])
        comments = GuideComment.objects(guideId=guide_id).all()
        comments = json.loads(comments.to_json())
        user_ids = list(set(map(lambda l: l['userId'], comments)))
        users = User.objects(id__in=user_ids).only("id", "nickname", "avatar").all()
        users = json.loads(users.to_json())
        for comment in comments:
            comment['_id'] = comment['_id']['$oid']
            for user in users:
                if user['_id']['$oid'] == comment['userId']:
                    comment['userInfo'] = {
                        "_id": user['_id']['$oid'],
                        "nickname": user['nickname'],
                        "avatar": user['avatar'],
                    }
        response = {
            'result': comments,
            'haveComment': False
        }
        if request.session['currentUser']['_id'] in user_ids:
            response['haveComment'] = True
        return JsonResponse(response)
    raise Http404


"""
    /comment/commentSceneLists/  获得所有景区和与其相关的评论(暂时不用)
    Method: POST
    JSON: {}
"""
def comment_scene_lists(request):
    # TODO 会到时候修改的,会有一个景区的id参数，不需要遍历两层
    if request.method == "POST":
        comments = json.loads(SceneComment.objects().all().to_json())
        # 取出要查询的景区id和评论人id然后得到一个去重的列表
        scene_ids = list(set(map(lambda l: l['sceneId'], comments)))
        user_ids = list(set(map(lambda l: l['userId'], comments)))
        scenes = json.loads(Scene.objects(id__in=scene_ids).all().to_json())
        users = json.loads(User.objects(id__in=user_ids).all().to_json())
        # 遍历comments这个列表然后把相关的景区信息和评论人的信息插进去
        for comment in comments:
            for scene in scenes:
                if scene['_id']['$oid'] == comment['sceneId']:
                    comment['sceneInfo'] = scene
            for user in users:
                if user['_id']['$oid'] == comment['userId']:
                    comment['userInfo'] = {
                        "_id": user['_id'],
                        "nickname": user['nickname'],
                        "avatar": user['avatar'],
                    }
        return JsonResponse({"result": comments})
    raise Http404


"""
    /comment/commentGuideLists/  获得所有导游与其相关的评论(暂时不用)
    Method: POST
    JSON: {}
"""
def comment_guide_lists(request):
    if request.method == "POST":
        comments = json.loads(GuideComment.objects().all().to_json())
        user_ids = list(set(map(lambda l: l['guideId'] or l['userId'], comments)))
        users = json.loads(User.objects(id__in=user_ids).all().to_json())
        # TODO 其实可能会有一个导游id参数，遍历会少一层,那么就不会这么麻烦了
        # for comment in comments:
        #     for user in users:
        #         if user['_id']['$oid'] == comment['guideId']:
        #             comment['guideInfo'] = {
        #                 "_id": user['_id'],
        #                 "nickname": user['nickname'],
        #                 "avatar": user['avatar'],
        #             }
        return JsonResponse({"result": comments})
    raise Http404


def test1(request):
    # del request.COOKIES
    # request.session['user'] = 21
    print request.COOKIES
    print request.session.__dict__
    print request.session.get('currentUser')
    http = JsonResponse({'result': 321})
    # http.delete_cookie('sessionid')
    # http.set_cookie('session', )
    return http


def test(request):
    # from django.contrib.sessions.backends.db import SessionStore
    # s = SessionStore(session_key=request.COOKIES['sessionid'])
    # print "123", s.session_key
    # time = datetime.datetime.now()
    # lists = SceneComment.objects(commentTime__gte=time)
    # for i in lists:
    #     print i.commentTime
    # return HttpResponse(lists.to_json())
    print request.COOKIES
    print request.session.__dict__
    print request.session.get('currentUser')
    # try:
    #     request.session['currentUser']
    # except KeyError:
    #     print 1236465465465
    http = JsonResponse({"results": 123})
    # http.delete_cookie('sessionid')
    # http.set_cookie("sessionid", {'user': 123})
    return http
    # return
