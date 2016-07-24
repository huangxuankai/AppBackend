# encoding:utf8
""" By Daath """

from django.conf.urls import url, patterns
import webViews

urlpatterns = patterns('',
    url(r'^signIn/', webViews.sign_in),
    url(r'^signUp/', webViews.sign_up),
    url(r'^signOut/', webViews.sign_out),
    url(r'^adminCenter/', webViews.admin_center),
    url(r'^applyGuideLists/', webViews.apply_guide_lists),
    url(r'^applyAdminLists/', webViews.apply_admin_lists),
    url(r'^becomeGuide/', webViews.become_guide),
    url(r'^becomeAdmin/', webViews.become_admin),
)


