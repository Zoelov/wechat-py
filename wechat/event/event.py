# -*-coding:utf-8 -*-
from __future__ import absolute_import
from xml.etree import ElementTree as ET
import logging
from wechat.service.user import get_users
from orm import models as orm_models
from django.conf import settings
from utils import public
import datetime
from django.http import HttpResponse

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

        if msg_type == 'event' and event == 'subscribe':
            logger.info(u'新用户关注，open_id=%s' % from_user_name)
            access_token = public.access_token()
            if access_token:
                user_info = get_users(access_token, from_user_name)
                if user_info:
                    user_obj = orm_models.User.objects.filter(id=from_user_name, subscribe=0)
                    if user_obj.exists():
                        user_info['unsubscribe_time'] = None
                        name = orm_models.User.objects.update_info(user_info)
                    else:
                        name = orm_models.User.objects.add_user(
                            user_info.get('openid'),
                            user_info.get('subscribe'),
                            user_info.get('nickname'),
                            user_info.get('sex'),
                            user_info.get('city'),
                            user_info.get('country'),
                            user_info.get('province'),
                            user_info.get('language'),
                            user_info.get('headimgurl'),
                            user_info.get('subscribe_time'),
                            user_info.get('unionid'),
                            user_info.get('remark'),
                            user_info.get('groupid')
                        )
                        logger.info(u'保存新用户信息成功')
                else:
                    logger.error(u'未查询到用户信息')
                    return None
            ret = public.replay_text(from_user_name, to_user_name, u'欢迎%s的关注！' % name)

            return ret
        elif msg_type == 'event' and event == 'unsubscribe':
            param = {
                'openid': from_user_name,
                'subscribe': 0,
                'unsubscribe_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            orm_models.User.objects.update_info(param)
            ret = public.replay_text(from_user_name, to_user_name, '')
            return ret
        else:
            return None
    except Exception as exc:
        logger.error(u'订阅信息处理发生异常,error msg:%s' % exc.message, exc_info=True)


def location_event(param):
    """
    地理位置事件处理
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
        latitude = tree.find('Latitude').text
        longitude = tree.find('Longitude').text
        precision = tree.find('Precision').text

        orm_models.UserLocation.objects.add_location(from_user_name, create_time, latitude, longitude, precision)
        ret = public.replay_text(from_user_name, to_user_name, '')

        return ret
    except Exception as exc:
        logger.error(u'处理地理位置信息发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc


def menu_event(param):
    """
    菜单事件处理
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
        key = tree.find('EventKey').text
        count = tree.find('Count').text if tree.find('Count') is not None else None

        menu_obj = orm_models.MenuEvent.objects.add_event(from_user_name, create_time, event, key, count)
        ret = public.replay_text(from_user_name, to_user_name, u'图片')
        return ret

        # 查询消息记录，找到图片并进行处理
        # obj = orm_models.RecMessage.objects.filter(from_user_id=from_user_name, create_time=menu_obj.create_time, is_reply=0)
        # if obj.exists():
        #     for index in obj:
        #         pass

    except Exception as exc:
        logger.error(u'处理菜单事件发生异常,error msg:%s' % exc.message, exc_info=True)
        raise exc


def process_event(param):
    """
    事件处理
    :param param:
    :return:
    """
    tree = ET.fromstring(param)
    event = tree.find('Event').text
    ret = ''
    if event == 'subscribe' or event == 'unsubscribe':
        ret = subscribe_or_unbscribe(param)

    if event == 'LOCATION':
        ret = location_event(param)

    if event in ('pic_photo_or_album', 'pic_sysphoto'):
        ret = menu_event(param)
    return HttpResponse(ret, content_type='application/xml')