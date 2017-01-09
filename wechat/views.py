# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context
from xml.dom.minidom import Document
from xml.etree import ElementTree as ET
import time
import hashlib
import logging
from orm import models as orm_models

# Create your views here.

logger = logging.getLogger(__name__)


def health(req):
    """
    health
    :param req:
    :return:
    """
    logger.info('health test')
    return HttpResponse('ok')


class WeChat(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WeChat, self).dispatch(*args, **kwargs)

    def get(self, request):
        logger.info('test......')
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        token = settings.TOKEN

        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashlib.sha1(hashstr).hexdigest()

        if hashstr == signature:
            return HttpResponse(echostr)

    def post(self, req):
        logger.info('接收到消息')
        logger.info('body=%s' % req.body)
        tree = ET.fromstring(req.body)
        user_name = tree.find('ToUserName').text if tree.find('ToUserName') else None
        from_user_name = tree.find('FromUserName').text if tree.find('FromUserName') else None
        create_time = tree.find('CreateTime').text if tree.find('CreateTime') else None
        msg_type = tree.find('MsgType').text if tree.find('MsgType') else None
        msg_id = tree.find('MsgId').text if tree.find('MsgId') else None
        msg = tree.find('Content').text if tree.find('Content') else None
        pic_url = tree.find('PicUrl').text if tree.find('PicUrl') else None
        media_id = tree.find('MediaId').text if tree.find('MediaId') else None
        format = tree.find('Format').text if tree.find('Format') else None
        recognition = tree.find('Recognition').text if tree.find('Recognition') else None
        thumb_media_id = tree.find('ThumbMediaId').text if tree.find('ThumbMediaId') else None
        location_x = tree.find('Location_X').text if tree.find('Location_X') else None
        location_y = tree.find('Location_Y').text if tree.find('Location_Y') else None
        scale = tree.find('Scale').text if tree.find('Scale') else None
        label = tree.find('Label').text if tree.find('Label') else None
        title = tree.find('Title').text if tree.find('Title') else None
        description = tree.find('Description').text if tree.find('Description') else None
        url = tree.find('Url').text if tree.find('Url') else None

        logger.info(vars())

        try:
            # 保存收到的消息
            orm_models.RecMessage.objects.add_msg(from_user_name, msg_type, create_time, msg, msg_id, pic_url, media_id,
                                                  format, recognition, thumb_media_id, location_x, location_y, scale,
                                                  label, title, description, url)
        except Exception as exc:
            logger.error(u'保存收到的消息失败，error msg:%s' % exc.message, exc_info=True)


        try:
            result = self.replay_text(from_user_name, user_name, u'哈哈')
            logger.info('replay is:%s' % result)
            return HttpResponse(result, content_type='application/xml')
        except Exception as exc:
            logger.error(u'发生异常，error msg:%s' % exc.message, exc_info=True)
            return HttpResponse('', content_type='application/xml')

    def replay_text(self, to_user_name, from_user_name, msg, msg_type='text'):
        """
        回复文本消息
        :param to_user_name:
        :param from_user_name:
        :param msg:
        :param msg_type:
        :return:
        """
        now = time.time()
        replay = """
            <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[%s]]></MsgType>
                <Content><![CDATA[%s]]></Content>
            </xml>
        """ % (to_user_name, from_user_name, str(int(now)), msg_type, msg)

        return replay


