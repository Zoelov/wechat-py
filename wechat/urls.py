# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('wechat',
                       url(r'^$', WeChat.as_view()),
                       url(r'^health?$', 'views.health'),
                       )