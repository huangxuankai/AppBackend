# encoding:utf8
""" By Daath """

from django.http import *
from django.shortcuts import render

from models import User, AdminUser
from appScene.models import Scene
from application.exception import resultMsg
from application.function import web_id_replace, admin_login_auth
import json


# Create your views here.

"""
    /admin/user/signUp/ 管理页面用户注册
    Method: POST
    Parameter: |  account password realName nickname phone
    JSON: {
        'error': False,
        'msgCode': 0,
        'msg': "sign up success"
    }
"""
def sign_up(request):
    if request.method == "GET":
        return render(request, 'signUp.html')
    if request.method == "POST":
        account = request.POST.get('account', None)
        password = request.POST.get('password', None)
        real_name = request.POST.get('realName', None)
        nickname = request.POST.get('nickname', None)
        phone = request.POST.get('phone', None)
        if not account or not password or not real_name or not nickname or not phone:
            return JsonResponse(resultMsg['NeedParameter'])
        is_exist = AdminUser.objects(account=account).filter().count()
        if is_exist:
            return JsonResponse(resultMsg['ExistUser'])
        admin_user = AdminUser()
        admin_user.account = account
        admin_user.password = password
        admin_user.realName = real_name
        admin_user.nickname = nickname
        admin_user.phone = phone
        admin_user.save()
        print account + "||" + password + "||" + real_name
        return JsonResponse(resultMsg['SignUpSuccess'])


"""
    /admin/user/signIn/ 管理页面用户登陆
    Method: POST
    Parameter: |  account password
    JSON: {
        'error': False,
        'msgCode': 4,
        'msg': "sign In success"
    }
"""
def sign_in(request):
    if request.method == "GET":
        return render(request, 'signIn.html')
    if request.method == "POST":
        account = request.POST.get('account', None)
        password = request.POST.get('password', None)
        if not account or not password:
            return JsonResponse(resultMsg['NeedParameter'])
        try:
            admin_user = AdminUser.objects(account=account).get()
        except AdminUser.DoesNotExist:
            return JsonResponse(resultMsg['NotExistUser'])
        if admin_user.status != "admin":
            return JsonResponse(resultMsg['AdminAuthorityApplying'])
        if admin_user.password == password:
            request.session['currentAdmin'] = {
                'id': str(admin_user.id),
                'nickname': admin_user.nickname,
                'realName': admin_user.realName,
                'avatar': admin_user.avatar,
                'status': admin_user.status
            }
            return JsonResponse(resultMsg['SignInSuccess'])
        else:
            return JsonResponse(resultMsg['ErrorPassword'])


"""
    /admin/user/signOut/ 管理页面用户退出
    Method: POST
"""
def sign_out(request):
    try:
        del request.session['currentAdmin']
    except KeyError:
        pass
    return HttpResponseRedirect('/admin/user/signIn/')


@admin_login_auth
def admin_center(request):
    scene_lists = Scene.objects().only('id', 'name', 'province', 'city', 'status').all()
    scene_lists = json.loads(scene_lists.to_json())
    map(web_id_replace, scene_lists)
    print scene_lists
    return render(request, 'adminCenter.html', {'scenes': scene_lists})


@admin_login_auth
def apply_guide_lists(request):
    apply_guides = User.objects(status="applyGuide").only('id', 'nickname', 'realName', 'status', 'phone').all()
    apply_guides = json.loads(apply_guides.to_json())
    map(web_id_replace, apply_guides)
    return render(request, 'applyGuideLists.html', {'applyGuides': apply_guides})


@admin_login_auth
def apply_admin_lists(request):
    apply_admins = AdminUser.objects(status="applyAdmin").only('id', 'nickname', 'realName', 'status', 'phone').all()
    apply_admins = json.loads(apply_admins.to_json())
    map(web_id_replace, apply_admins)
    return render(request, 'applyAdminLists.html', {'applyAdmins': apply_admins})


@admin_login_auth
def become_guide(request):
    if request.method == "POST":
        user_id = request.POST.get('id', None)
        if not user_id:
            return JsonResponse(resultMsg['NeedParameter'])
        User.objects.get(id=user_id).update(status="guide")
        return JsonResponse(resultMsg['BecomeGuide'])
    raise Http404


@admin_login_auth
def become_admin(request):
    if request.method == "POST":
        admin_id = request.POST.get('id', None)
        if not admin_id:
            return JsonResponse(resultMsg['NeedParameter'])
        AdminUser.objects.get(id=admin_id).update(status="admin")
        print resultMsg['BecomeAdmin']
        return JsonResponse(resultMsg['BecomeAdmin'])
    raise Http404
