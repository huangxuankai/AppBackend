# encoding:utf8
""" By Daath """

from django.conf.urls import url, patterns
import views

urlpatterns = patterns('',
    url(r'^commentScene/', views.comment_scene),
    url(r'^commentGuide/', views.comment_guide),

    url(r'^getSceneComment/', views.get_scene_comment),
    url(r'^getGuideComment/', views.get_guide_comment),

    # url(r'^commentSceneLists/', views.comment_scene_lists),
    # url(r'^commentGuideLists/', views.comment_guide_lists),

    # 测试接口
    url(r'^test1/', views.test1),
    url(r'^test/', views.test)
)
