# encoding:utf8
""" By Daath """

from django.conf.urls import url, patterns
import views

urlpatterns = patterns('',
    url(r'^signCheck/', views.sign_check),
    url(r'^signUp/', views.sign_up),
    url(r'^signIn/', views.sign_in),
    url(r'^signOut/', views.sign_out),
    url(r'^update/', views.update),
    url(r'^updateLocation/', views.update_location),
    url(r'^modifyPassword/', views.modify_password),
    url(r'^applyGuide/', views.apply_guide),
    url(r'^getGuideLists/', views.get_guide_lists),
    url(r'^getVisitorLists/', views.get_visitor_lists),
    # url(r'^getVisitorInfo/', views.get_visitor_info), 没用到
    url(r'^avatarUpload/', views.avatar_upload),
    url(r'^tokenReload/', views.token_reload),
    url(r'^saveChannelId/', views.save_channel_id),

    # 测试接口
    url(r'^test/', views.test),
    url(r'^imageTest/', views.image_test),


)
