# -*- coding:utf-8 -*-

import hashlib
import logging
from multiprocessing import Process
from xml.etree import ElementTree as ET

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from utils import public
from wechat.event import event
from wechat.msg import msg

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


def work(param):
    """

    :param param:
    :return:
    """
    tree = ET.fromstring(param)
    msg_type = tree.find('MsgType').text if tree.find('MsgType') is not None else None
    if msg_type == 'event':
        p1 = Process(target=event.process_event, args=(param,))
        p1.start()
        p1.join()
    else:
        return msg.process_msg(param)


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
        tree = ET.fromstring(req.body)
        user_name = tree.find('ToUserName').text if tree.find('ToUserName') is not None else None
        from_user_name = tree.find('FromUserName').text if tree.find('FromUserName') is not None else None
        msg_type = tree.find('MsgType').text if tree.find('MsgType') is not None else None

        try:
            ret = work(req.body)
        except Exception as exc:
            logger.error(u'保存收到的消息失败，error msg:%s' % exc.message, exc_info=True)
        return HttpResponse(ret, content_type='application/xml')

