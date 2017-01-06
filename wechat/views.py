# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context
from xml.etree import ElementTree as ET
import time
import hashlib
import logging


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

        token = "wanghaotoken"

        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashlib.sha1(hashstr).hexdigest()

        if hashstr == signature:
            return HttpResponse(echostr)

    def post(self, req):
        logger.info('接收到消息')
        user_name = req.POST.get('ToUserName')
        from_user_name = req.POST.get('FromUserName')
        create_time = req.POST.get('CreateTime')
        msg_type = req.POST.get('MsgType')
        msg = req.POST.get('Content')
        msg_id = req.POST.get('MsgId')

        logger.info(vars())


