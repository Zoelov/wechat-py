# coding=utf-8
from django.db import models
from utils import public
from orm.manager.user import  UsersManager, AccessManager
from orm.manager.msg import RepManager, RecManager

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
IS_VALID = (
    ('0', u'无效',),
    ('1', u'有效',),
)

MSG_TYPE = (
    ('0', 'text',),
    ('1', 'image',),
    ('2', 'voice',),
    ('3', 'video',),
    ('4', 'shortvideo',),
    ('5', 'location',),
    ('6', 'link',),
)


# class OpenInfo(models.Model):
#     id = models.CharField('open id', max_length=64, primary_key=True)
#     total = models.IntegerField('total ', help_text=u'关注者总数')
#     count = models.IntegerField('count', help_text=u'拉取的openid个数')
#     next_openid = models.CharField('next open id', max_length=64, blank=True, null=True)
#
#     objects = OpenInfoManager()
#
#     class Meta:
#         db_table = 'wechat_open_info'


class User(models.Model):
    id = models.CharField('open id', primary_key=True, max_length=64)
    subscribe = models.BooleanField('subscribe', choices=IS_SUBSCRIBE, default=1)
    nickname = models.CharField('nickname', max_length=36)
    sex = models.CharField('sex', choices=SEX, default=0, max_length=1)
    city = models.CharField('city', max_length=36)
    country = models.CharField('country', max_length=36)
    province = models.CharField('province', max_length=36)
    language = models.CharField('language', max_length=36)
    headimgurl = models.CharField('head', max_length=200)
    subscribe_time = models.DateTimeField('subscribe_time', auto_now_add=True, help_text=u'关注时间')
    unionid = models.CharField('unionid', blank=True, null=True, max_length=36)
    remark = models.CharField('remark', max_length=36, help_text=u'对关注者的备注')
    groupid = models.CharField('groupid', max_length=36)

    objects = UsersManager()

    class Meta:
        db_table = 'wechat_user'


class AccessToken(models.Model):
    id = models.IntegerField(primary_key=True, help_text='token', db_column='id')
    access_token = models.CharField('access token', max_length=512)
    create_time = models.DateTimeField('create_time', auto_now_add=True, help_text=u'创建时间')
    expires_time = models.IntegerField(help_text=u'过期时间，单位为秒')
    end_time = models.DateTimeField('end_time', db_column='end_time')
    is_valid = models.BooleanField('is_valid', choices=IS_VALID, default=1)

    objects = AccessManager()

    class Meta:
        db_table = 'wechat_access_token'


class RecMessage(models.Model):
    id = models.CharField('msg id', max_length=36, primary_key=True, default=public.create_uuid('msg'))
    from_user = models.ForeignKey(User)
    msg_type = models.CharField('msg type', choices=MSG_TYPE, default=0, max_length=2, help_text=u'消息类型')
    create_time = models.DateTimeField('create_time', help_text=u'消息的创建时间')
    msg_content = models.TextField('msg content', null=True, blank=True, help_text=u'text类型消息内容')
    msg_id = models.CharField('msg id', max_length=64, help_text=u'消息id')
    pic_url = models.CharField('pic url', max_length=200, null=True, blank=True, help_text=u'图片链接')
    media_id = models.CharField('media id', null=True, blank=True, max_length=64, help_text=u'图片消息媒体id')
    format = models.CharField('format', null=True, blank=True, max_length=16, help_text=u'语音格式')
    recognition = models.TextField(help_text=u'语音识别结果', null=True, blank=True)
    thumb_media_id = models.CharField('thumb media id', null=True, blank=True, max_length=64, help_text=u'视频消息缩略图的媒体id')
    location_x = models.FloatField('location x', null=True, blank=True, help_text=u'地理位置维度')
    location_y = models.FloatField('location y', null=True, blank=True, help_text=u'地理位置经度')
    scale = models.FloatField('scale', null=True, blank=True, help_text=u'地图缩放大小')
    label = models.TextField('label', null=True, blank=True, help_text=u'地理位置信息')
    title = models.CharField('title', max_length=100, null=True, blank=True, help_text=u'消息标题')
    description = models.CharField('description', max_length=100, null=True, blank=True, help_text=u'消息描述')
    url = models.CharField('url', max_length=200, null=True, blank=True, help_text=u'消息链接')

    objects = RecManager()

    class Meta:
        db_table = 'wechat_rec_message'


class ReplayMessage(models.Model):
    id = models.CharField('msg id', max_length=36, primary_key=True, default=public.create_uuid('msg'))
    rec = models.ForeignKey(RecMessage)
    to_user = models.ForeignKey(User)
    msg_type = models.CharField('msg type', choices=MSG_TYPE, default=0, max_length=2, help_text=u'消息类型')
    create_time = models.DateTimeField('create_time', help_text=u'消息的创建时间')
    msg_content = models.TextField('msg content', null=True, blank=True, help_text=u'text类型消息内容')
    media_id = models.CharField('media id', null=True, blank=True, max_length=64, help_text=u'图片消息媒体id')
    title = models.CharField('title', max_length=100, null=True, blank=True, help_text=u'消息标题')
    description = models.CharField('description', max_length=100, null=True, blank=True, help_text=u'消息描述')
    music_url = models.CharField('url', max_length=200, null=True, blank=True, help_text=u'音乐链接')
    hq_music_url = models.CharField('url', max_length=200, null=True, blank=True, help_text=u'高质量音乐链接')
    thumb_media_id = models.CharField('thumb media id', null=True, blank=True, max_length=64, help_text=u'视频消息缩略图的媒体id')
    article_count = models.IntegerField(blank=True, null=True, help_text=u'图文消息个数')
    articles = models.CharField('articles', max_length=200, null=True, blank=True)
    pic_url = models.CharField('pic url', max_length=200, null=True, blank=True, help_text=u'图片链接')
    url = models.CharField('url', max_length=200, null=True, blank=True, help_text=u'跳转链接')

    objects = RepManager()

    class Meta:
        db_table = 'wechat_replay_message'










