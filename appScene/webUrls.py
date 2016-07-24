# encoding:utf8
""" By Daath """

from django.conf.urls import url, patterns
import webViews

urlpatterns = patterns('',
    url(r'^add/', webViews.add),
    url(r'^update/', webViews.update),
    url(r'^updateStatus/', webViews.update_status),
    url(r'^query/', webViews.query)
)
