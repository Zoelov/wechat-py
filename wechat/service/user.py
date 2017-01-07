# -*- coding:utf-8 -*-
from django.conf import settings
import logging
import httplib2 as http
import json
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class RequestAPI():
    STATUS_CODE = {
        '200': '成功',
        '201': '成功',
        '404': '资源不存在',
        '409': '资源冲突，存在关键资源',
        '500': '服务不可用'
    }

    @classmethod
    def access_data(cls, url, method, body='', token=''):
        if url == '':
            return {'status': '2001', 'msg': 'path is empty!'}
        if method.upper() not in ('GET', 'POST', 'DELETE', 'PUT'):
            return {'status': '2002', 'msg': 'method is invalid!'}

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        }
        if token:
            headers['Access-Token'] = token

        target = urlparse(url)

        # print(target.geturl())
        logger.info(u'调用API url: %s', target.geturl())

        h = http.Http()

        if not isinstance(body, str):
            body = json.dumps(body)
        body = '' if method in ['GET'] else body
        logger.info('调用底层参数: %s', body)
        try:
            response, content = h.request(target.geturl(), method, body, headers)
        except Exception as exc:
            logger.error('请求底层失败，error msg:%s' % exc.message, exc_info=True)
            response, content = h.request(target.geturl(), method, body, headers)
        logger.info('底层返回状态: %s, 结果: %s', str(response.status), content)
        # if method in ['POST', 'PUT']:
        #     response = requests.request(method, target.geturl(), json=body, headers=headers)
        # else:
        #     response = requests.request(method, target.geturl(), headers=headers)
        rtn_status = response.status

        try:
            try:
                data = json.loads(content)
            except Exception as exc:
                logger.error('json转化底层数据失败, raise Exception: %r' % exc)
                data = eval(content)
        except Exception as exc:
            logger.error('json转化底层数据失败, raise Exception: %r' % exc)
            data = content
        logger.info('返回结果: %s', data)
        return {'status': rtn_status, 'data': data, 'msg': cls.STATUS_CODE.get(rtn_status, '')}


def get_access_token(app_id, app_secret):
    """
    获取公众号的access_token
    :param app_id:
    :param app_secret:
    :return:
    """
    url = settings.ACCESS_TOKEN_URL + '&appid=%s&secret=%s' % (app_id, app_secret)
    logger.info('url=%s' % url)

    try:
        ret = RequestAPI.access_data(url, 'GET')
        if ret.get('status') == 200:
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
    if next_openid is None:
        url = settings.ACCESS_OPEN_ID + 'access_token=%s&next_openid=' % access_token
    else:
        url = settings.ACCESS_OPEN_ID + 'access_token=%s&next_openid=%s' % (access_token, next_openid)
    logger.info('url = %s' % url)
    try:
        ret = RequestAPI.access_data(url, 'GET')
        if ret.get('status') == 200:
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
    url = settings.ACCESS_USER_URL + 'access_token=%s&openid=%s&lang=%s' % (access_token, open_id, lang)

    try:
        ret = RequestAPI.access_data(url, 'GET')
        if ret.get('status') == 200:
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






