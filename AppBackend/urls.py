# encoding:utf8
""" By Daath """

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # url(r'^home/visitorLists/', views.visitor_lists),
    # url(r'^home/guideLists/', views.guide_lists),

    # api接口
    url(r'^api/user/', include('appUser.urls')),
    url(r'^api/scene/', include('appScene.urls')),
    url(r'^api/comment/', include('appComment.urls')),

    # web接口
    url(r'^admin/home/', views.home),
    url(r'^admin/user/', include('appUser.webUrls')),
    url(r'^admin/scene/', include('appScene.webUrls')),

)
