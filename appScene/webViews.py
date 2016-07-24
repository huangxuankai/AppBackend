# encoding:utf8
""" By Daath """
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import *
from .models import Scene, SceneImage
from application.exception import resultMsg, prefURL
from application.function import produce_image_name, admin_login_auth

# Create your views here.


@admin_login_auth
def add(request):
    if request.method == "GET":
        return render(request, 'addScene.html')
    if request.method == "POST":
        name = request.POST.get('sceneName', None)
        description = request.POST.get('sceneDescription', None)
        city = request.POST.get('sceneCity', None)
        province = request.POST.get('sceneProvince', None)
        if not name or not description or not city or not province:
            return JsonResponse(resultMsg['NeedParameter'])

        try:
            latitude = float(request.POST.get('sceneLatitude', None))
            longitude = float(request.POST.get('sceneLongitude', None))
            coordinates = [longitude, latitude]     # 做成坐标组
        except:
            return JsonResponse(resultMsg['CoordinatesError'])

        try:
            image = request.FILES['sceneImage']
        except:
            return JsonResponse(resultMsg['NeedSceneImage'])

        is_exist = Scene.objects(name=name).filter().count()
        if is_exist:
            return JsonResponse(resultMsg['ExistScene'])
        print image.content_type
        # 图片缓存
        scene_image = SceneImage()
        if image.content_type == 'image/png':
            print image.content_type
            scene_image.image.save(produce_image_name() + '.png', image)
        if image.content_type == 'image/jpg' or image.content_type == 'image/jpeg':
            print image.content_type
            scene_image.image.save(produce_image_name() + '.jpg', image)
        print scene_image.image

        scene = Scene()
        scene.name = name
        scene.description = description
        scene.city = city
        scene.province = province
        scene.location = coordinates
        scene.image = prefURL['ImageURL'] + scene_image.image.__str__()
        scene.save()

        return JsonResponse(resultMsg['addSceneSuccess'])


@admin_login_auth
def update(request):
    if request.method == "POST":
        scene_id = request.POST.get('id', None)
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        city = request.POST.get('city', None)
        province = request.POST.get('province', None)
        if not scene_id or not name or not name or not description or not city or not province:
            return JsonResponse(resultMsg['NeedParameter'])
        try:
            latitude = float(request.POST.get('latitude', None))
            longitude = float(request.POST.get('longitude', None))
            coordinates = [longitude, latitude]     # 做成坐标组
        except:
            return JsonResponse(resultMsg['CoordinatesError'])

        is_exist = Scene.objects(name=name).filter()
        if is_exist and str(is_exist[0].id) != scene_id:
            return JsonResponse(resultMsg['ExistScene'])

        update_dict = dict()
        update_dict['name'] = name
        update_dict['description'] = description
        update_dict['city'] = city
        update_dict['province'] = province
        update_dict['location'] = coordinates
        scene = Scene.objects(id=scene_id).get()
        scene.update(**update_dict)
        return JsonResponse(resultMsg['updateSceneSuccess'])
    raise Http404


@admin_login_auth
def update_status(request):
    if request.method == "POST":
        scene_id = request.POST.get('id', None)
        status = request.POST.get('status', None)
        if not scene_id or not status:
            return JsonResponse(resultMsg['NeedParameter'])
        if not (status in ['online', 'offline']):
            return JsonResponse(resultMsg['StatusValueError'])
        Scene.objects(id=scene_id).get().update(status=status)
        response = {
            'online': resultMsg['onlineSceneSuccessful'],
            'offline': resultMsg['offlineSceneSuccessful']
        }
        return JsonResponse(response[status])
    raise Http404


@admin_login_auth
def query(request):
    scene_id = request.GET.get('id', None)
    if not scene_id:
        return JsonResponse(resultMsg['NeedParameter'])
    scene = Scene.objects.get(id=scene_id)
    return render(request, 'sceneDetail.html', {'scene': scene.data_clean()})
