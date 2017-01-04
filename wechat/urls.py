# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import WeChat

urlpatterns = patterns('',
                       url(r'^$', WeChat.as_view()),
                       )