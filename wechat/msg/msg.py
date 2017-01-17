# -*- coding:utf-8 -*-
from xml.etree import ElementTree as ET
import logging
from orm import models as orm_models
from utils import public
from django.http import HttpResponse


logger = logging.getLogger(__name__)


def text(param):
    logger.info(param)
    tree = ET.fromstring(param)
    user_name = tree.find('ToUserName').text if tree.find('ToUserName') is not None else None
    from_user_name = tree.find('FromUserName').text if tree.find('FromUserName') is not None else None
    create_time = tree.find('CreateTime').text if tree.find('CreateTime') is not None else None
    msg_type = tree.find('MsgType').text if tree.find('MsgType') is not None else None
    msg_id = tree.find('MsgId').text if tree.find('MsgId') is not None else None
    msg = tree.find('Content').text if tree.find('Content') is not None else None
    try:
        obj = orm_models.RecMessage.objects.add_msg(from_user_name, msg_type, create_time, msg_id, msg)
        ret = public.replay_text(from_user_name, user_name, u'哈哈')
        orm_models.RecMessage.objects.update_status(obj, 1)
        return ret
    except Exception as exc:
        logger.error(u'处理消息发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc


def image(param):
    """
    图片消息
    :param param:
    :return:
    """
    logger.info(param)
    tree = ET.fromstring(param)
    user_name = tree.find('ToUserName').text if tree.find('ToUserName') is not None else None
    from_user_name = tree.find('FromUserName').text if tree.find('FromUserName') is not None else None
    create_time = tree.find('CreateTime').text if tree.find('CreateTime') is not None else None
    msg_type = tree.find('MsgType').text if tree.find('MsgType') is not None else None
    msg_id = tree.find('MsgId').text if tree.find('MsgId') is not None else None
    pic_url = tree.find('PicUrl').text if tree.find('PicUrl') is not None else None
    media_id = tree.find('MediaId').text if tree.find('MediaId') is not None else None
    try:
        obj = orm_models.RecMessage.objects.add_msg(from_user_name, msg_type, create_time, msg_id, None, pic_url, media_id)
        ret = public.replay_text(from_user_name, user_name, u'哈哈')
        orm_models.RecMessage.objects.update_status(obj, 1)
        return ret
    except Exception as exc:
        logger.error(u'处理消息发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc


def voice(param):
    """
    处理语音消息
    :param param:
    :return:
    """
    logger.info(param)
    tree = ET.fromstring(param)
    user_name = tree.find('ToUserName').text if tree.find('ToUserName') is not None else None
    from_user_name = tree.find('FromUserName').text if tree.find('FromUserName') is not None else None
    create_time = tree.find('CreateTime').text if tree.find('CreateTime') is not None else None
    msg_type = tree.find('MsgType').text if tree.find('MsgType') is not None else None
    msg_id = tree.find('MsgId').text if tree.find('MsgId') is not None else None
    media_id = tree.find('MediaId').text if tree.find('MediaId') is not None else None
    format = tree.find('Format').text if tree.find('Format') is not None else None
    recognition = tree.find('Recognition').text if tree.find('Recognition') is not None else None
    try:
        obj = orm_models.RecMessage.objects.add_msg(from_user_name, msg_type, create_time, msg_id, None, None, media_id, format, recognition)
        ret = public.replay_text(from_user_name, user_name, u'哈哈')
        orm_models.RecMessage.objects.update_status(obj, 1)
        return ret
    except Exception as exc:
        logger.error(u'处理消息发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc


def video(param):
    """
    视频消息
    :param param:
    :return:
    """
    logger.info(param)
    tree = ET.fromstring(param)
    user_name = tree.find('ToUserName').text if tree.find('ToUserName') is not None else None
    from_user_name = tree.find('FromUserName').text if tree.find('FromUserName') is not None else None
    create_time = tree.find('CreateTime').text if tree.find('CreateTime') is not None else None
    msg_type = tree.find('MsgType').text if tree.find('MsgType') is not None else None
    msg_id = tree.find('MsgId').text if tree.find('MsgId') is not None else None
    media_id = tree.find('MediaId').text if tree.find('MediaId') is not None else None
    thumb_media_id = tree.find('ThumbMediaId').text if tree.find('ThumbMediaId') is not None else None
    try:
        obj = orm_models.RecMessage.objects.add_msg(from_user_name, msg_type, create_time, msg_id, None, None, media_id
                                                    , None, None, thumb_media_id)
        ret = public.replay_text(from_user_name, user_name, u'哈哈')
        orm_models.RecMessage.objects.update_status(obj, 1)
        return ret
    except Exception as exc:
        logger.error(u'处理消息发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc


def location(param):
    """
    处理地理位置消息
    :param param:
    :return:
    """
    logger.info(param)
    tree = ET.fromstring(param)
    user_name = tree.find('ToUserName').text if tree.find('ToUserName') is not None else None
    from_user_name = tree.find('FromUserName').text if tree.find('FromUserName') is not None else None
    create_time = tree.find('CreateTime').text if tree.find('CreateTime') is not None else None
    msg_type = tree.find('MsgType').text if tree.find('MsgType') is not None else None
    msg_id = tree.find('MsgId').text if tree.find('MsgId') is not None else None
    location_x = tree.find('Location_X').text if tree.find('Location_X') is not None else None
    location_y = tree.find('Location_Y').text if tree.find('Location_Y') is not None else None
    scale = tree.find('Scale').text if tree.find('Scale') is not None else None
    label = tree.find('Label').text if tree.find('Label') is not None else None
    try:
        obj = orm_models.RecMessage.objects.add_msg(from_user_name, msg_type, create_time, msg_id, None, None, None
                                                    , None, None, None, location_x, location_y, scale, label)
        ret = public.replay_text(from_user_name, user_name, u'哈哈')
        orm_models.RecMessage.objects.update_status(obj, 1)
        return ret
    except Exception as exc:
        logger.error(u'处理消息发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc


def link(param):
    """
    处理链接消息
    :param param:
    :return:
    """
    logger.info(param)
    tree = ET.fromstring(param)
    user_name = tree.find('ToUserName').text if tree.find('ToUserName') is not None else None
    from_user_name = tree.find('FromUserName').text if tree.find('FromUserName') is not None else None
    create_time = tree.find('CreateTime').text if tree.find('CreateTime') is not None else None
    msg_type = tree.find('MsgType').text if tree.find('MsgType') is not None else None
    msg_id = tree.find('MsgId').text if tree.find('MsgId') is not None else None
    title = tree.find('Title').text if tree.find('Title') is not None else None
    description = tree.find('Description').text if tree.find('Description') is not None else None
    url = tree.find('Url').text if tree.find('Url') is not None else None
    try:
        obj = orm_models.RecMessage.objects.add_msg(from_user_name, msg_type, create_time, msg_id, None, None, None
                                                    , None, None, None, None, None, None, None, title, description, url)
        ret = public.replay_text(from_user_name, user_name, u'哈哈')
        orm_models.RecMessage.objects.update_status(obj, 1)
        return ret
    except Exception as exc:
        logger.error(u'处理消息发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc


def process_msg(param):
    """
    处理收到的消息
    :param param:
    :return:
    """
    tree = ET.fromstring(param)
    user_name = tree.find('ToUserName').text if tree.find('ToUserName') is not None else None
    from_user_name = tree.find('FromUserName').text if tree.find('FromUserName') is not None else None
    create_time = tree.find('CreateTime').text if tree.find('CreateTime') is not None else None
    msg_type = tree.find('MsgType').text if tree.find('MsgType') is not None else None

    ret = ''
    try:
        if msg_type == 'text':
            ret = text(param)

        if msg_type == 'image':
            ret = image(param)

        if msg_type == 'voice':
            ret = voice(param)

        if msg_type in ('video', 'shortvideo'):
            ret = video(param)

        if msg_type == 'location':
            ret = location(param)

        if msg_type == 'link':
            ret = link(param)
    except Exception as exc:
        logger.error(u'异常,error msg:%s'% exc.message, exc_info=True)
    return HttpResponse(ret, content_type='application/xml')
