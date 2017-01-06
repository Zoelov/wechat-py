# coding=utf-8
from django.db import models
from utils import public
from orm.manager.user import OpenInfoManager

# Create your models here.

import logging

logger = logging.getLogger(__name__)

IS_SUBSCRIBE = (
    ('0', 'not subscribe',),
    ('1', 'subscribe',),
)
SEX = (
    ('0', 'unknown',),
    ('1', 'male',),
    ('2', 'female',),
)


class OpenInfo(models.Model):
    id = models.CharField('open id', max_length=64, primary_key=True)
    total = models.IntegerField('total ', help_text=u'关注者总数')
    count = models.IntegerField('count', help_text=u'拉取的openid个数')
    next_openid = models.CharField('next open id', max_length=64, blank=True, null=True)

    objects = OpenInfoManager()

    class Meta:
        db_table = 'wechat_open_info'


class User(models.Model):
    id = models.CharField('User id', max_length=36, primary_key=True, default=public.create_uuid('user'),
                          help_text='user list')
    open = models.ForeignKey(OpenInfo, blank=True, null=True)
    subscribe = models.BooleanField('subscribe', choices=IS_SUBSCRIBE, default=1)
    nickname = models.CharField('nickname', max_length=36)
    sex = models.BooleanField('sex', choices=SEX, default=0)
    city = models.CharField('city', max_length=36)
    country = models.CharField('country', max_length=36)
    province = models.CharField('province', max_length=36)
    language = models.CharField('language', max_length=36)
    headimgurl = models.CharField('head', max_length=200)
    subscribe_time = models.DateTimeField('subscribe_time', auto_now_add=True, help_text=u'关注时间')
    unionid = models.CharField('unionid', blank=True, null=True, max_length=36)
    remark = models.CharField('remark', max_length=36, help_text=u'对关注者的备注')
    groupid = models.CharField('groupid', max_length=36)

    class Meta:
        db_table = 'wechat_user'







