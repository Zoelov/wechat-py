# -*- coding:utf-8 -*-
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def get_access_token(app_id, app_secret):
    """
    获取公众号的access_token
    :param app_id:
    :param app_secret:
    :return:
    """
    from utils.public import RequestAPI
    url = settings.ACCESS_TOKEN_URL + '&appid=%s&secret=%s' % (app_id, app_secret)
    logger.info('url=%s' % url)

    try:
        ret = RequestAPI.access_data(url, 'GET')
        if ret.get('status') == 200 and not ret.get('data').get('errcode'):
            logger.info(u'获取公众号token成功')
            return ret.get('data')
        else:
            logger.error(u'获取公众号token失败，error code=%s errormsg:%s' % (ret.get('data').get('errcode'), ret.get('data').get('errmsg')))
            return None
    except Exception as exc:
        logger.error(u'获取公众号token异常，error msg:%s' % exc.message, exc_info=True)
        raise exc


def get_open_id(access_token, next_openid):
    """
    获取openid
    """
    from utils.public import RequestAPI
    if next_openid is None:
        url = settings.ACCESS_OPEN_ID + 'access_token=%s&next_openid=' % access_token
    else:
        url = settings.ACCESS_OPEN_ID + 'access_token=%s&next_openid=%s' % (access_token, next_openid)
    logger.info('url = %s' % url)
    try:
        ret = RequestAPI.access_data(url, 'GET')
        if ret.get('status') == 200 and not ret.get('data').get('errcode'):
            logger.info(u'获取openid成功')
            return ret.get('data')
        else:
            logger.error(u'获取openid失败，errcode=%s errormsg:%s' % (ret.get('data').get('errcode'),ret.get('data').get('errmsg')))
            return None
    except Exception as exc:
        logger.error(u'获取openid发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc


def get_users(access_token, open_id, lang='zh_CN'):
    """
    获取用户信息
    """
    from utils.public import RequestAPI
    url = settings.ACCESS_USER_URL + 'access_token=%s&openid=%s&lang=%s' % (access_token, open_id, lang)
    logger.info(url)

    try:
        ret = RequestAPI.access_data(url, 'GET')
        if ret.get('status') == 200 and not ret.get('data').get('errcode'):
            logger.info(u'获取用户信息成功')
            return ret.get('data')
        else:
            logger.error(u'获取用户信息失败, errcode=%s errormsg:%s' % (
                ret.get('data').get('errcode'), ret.get('data').get('errmsg')
            ))
            return None
    except Exception as exc:
        logger.error(u'获取用户信息发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc






