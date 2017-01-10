# -*- coding:utf-8 -*-

import uuid
import datetime
from django.conf import settings
import logging
import time
from wechat.service.user import get_access_token

logger = logging.getLogger(__name__)


def create_uuid(name=''):
    '''
    自动生成36位uuid
    :param name:
    :return:
    '''
    return str(uuid.uuid1())


def access_token():
    """
    获取access_token
    :return:
    """
    from orm import models as orm_models
    try:
        now = datetime.datetime.now
        access = orm_models.AccessToken.objects.filter(is_valid=1, end_time__gt=now)
        if access.exists():
            return access[0].access_token
        else:
            orm_models.AccessToken.objects.set_invalid()
            token = get_access_token(settings.USER_APP_ID, settings.USER_APP_SECRET)
            if token:
                logger.info(u'获取access_token成功')
                logger.info('token = %s' % token)
                access_token = token.get('access_token')
                expires = token.get('expires_in')

                # 保存token信息
                now = datetime.datetime.now()
                end_time = now + datetime.timedelta(seconds=expires)
                orm_models.AccessToken.objects.add_token(access_token, expires, now, end_time)

                return access_token
            else:
                logger.error(u'调接口获取access_token失败')
                return None
    except Exception as exc:
        logger.error(u'获取access_token发生异常,error msg:%s' % exc.message, exc_info=True)
        raise exc


def replay_text(to_user_name, from_user_name, msg, msg_type='text'):
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