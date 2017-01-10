# -*-coding:utf-8 -*-
from __future__ import absolute_import
from xml.etree import ElementTree as ET
import logging
from wechat.service.user import get_users
from orm import models as orm_models
from django.conf import settings
from utils import public
import datetime

logger = logging.getLogger(__name__)


def subscribe_or_unbscribe(param):
    """
    订阅获取取消订阅公众号事件
    :param param:
    :return:
    """
    logger.info('param = %s' % param)
    try:
        tree = ET.fromstring(param)
        to_user_name = tree.find('ToUserName').text
        from_user_name = tree.find('FromUserName').text
        create_time = tree.find('CreateTime').text
        msg_type = tree.find('MsgType').text
        event = tree.find('Event').text

        if msg_type is 'event' and event is 'subscribe':
            logger.info(u'新用户关注，open_id=%s' % from_user_name)
            access_token = public.get_access_token()
            if access_token:
                user_info = get_users(access_token, from_user_name)
                if user_info:
                    user_obj = orm_models.User.objects.filter(id=from_user_name, subscribe=0)
                    if user_obj.exists():
                        user_obj[0]['unsubscribe_time'] = None
                        name = orm_models.User.objects.update_info(user_obj[0])
                    else:
                        name = orm_models.User.objects.add_user(
                            user_obj[0].get('openid'),
                            user_obj[0].get('subscribe'),
                            user_obj[0].get('nickname'),
                            user_obj[0].get('sex'),
                            user_obj[0].get('city'),
                            user_obj[0].get('country'),
                            user_obj[0].get('province'),
                            user_obj[0].get('language'),
                            user_obj[0].get('headimgurl'),
                            user_obj[0].get('subscribe_time'),
                            user_obj[0].get('unionid'),
                            user_obj[0].get('remark'),
                            user_obj[0].get('groupid')
                        )
                        logger.info(u'保存新用户信息成功')
            ret = public.replay_text(from_user_name, to_user_name, '欢迎您的%s关注！' % name)

            return ret
        elif msg_type is 'event' and event is 'unsubscribe':
            param = {
                'openid': from_user_name,
                'subscribe': 0,
                'unsubscribe_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            orm_models.User.objects.update_info(param)
            ret = public.replay_text(from_user_name, to_user_name, '别取关啊。。。')
            return ret
        else:
            return None
    except Exception as exc:
        logger.error(u'订阅信息处理发生异常,error msg:%s' % exc.message, exc_info=True)


def process_event(param):
    """
    事件处理
    :param param:
    :return:
    """
    tree = ET.fromstring(param)
    event = tree.find('Event').text
    if event is 'subscribe' or 'unsubscribe':
        return subscribe_or_unbscribe(param)