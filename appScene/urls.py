# encoding:utf8
""" By Daath """

from django.conf.urls import url, patterns
import views

urlpatterns = patterns('',

    url(r'^lists/', views.scene_lists),
    url(r'^search/', views.scene_search),

    # 测试接口
    url(r'^test/', views.test)
)
