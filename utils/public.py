# -*- coding:utf-8 -*-

import uuid
import datetime
from django.conf import settings
import logging
import time
from wechat.service.user import get_access_token
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


def replaty_images(to_user_name, from_user_name, media_id, msg_type='image'):
    """
    回复图片消息
    :param to_user_name:
    :param from_user_name:
    :param media_id:
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
            <Image>
                <MediaId><![CDATA[%s]]></MediaId>
            </Image>
            </xml>
    """ % (to_user_name, from_user_name, str(int(now)), msg_type, media_id)
    return replay


def replaty_voice(to_user_name, from_user_name, media_id, msg_type='voice'):
    """
    回复声音消息
    :param to_user_name:
    :param from_user_name:
    :param media_id:
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
            <Voice>
                <MediaId><![CDATA[%s]]></MediaId>
            </Voice>
            </xml>
    """ % (to_user_name, from_user_name, str(int(now)), msg_type, media_id)
    return replay


def replaty_video(to_user_name, from_user_name, media_id, title, description, msg_type='video'):
    """
    回复视频消息
    :param description:
    :param title:
    :param to_user_name:
    :param from_user_name:
    :param media_id:
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
            <Video>
                <MediaId><![CDATA[%s]]></MediaId>
                <Title><![CDATA[%s]]></Title>
                <Description><!CDATA[%s]]></Description>
            </Video>
            </xml>
    """ % (to_user_name, from_user_name, str(int(now)), msg_type, media_id, title, description)
    return replay


def replaty_music(to_user_name, from_user_name, title, description, music_url, hq_music_url, thumb_media_id,
                  msg_type='video'):
    """
    回复音乐消息
    :param thumb_media_id:
    :param hq_music_url:
    :param music_url:
    :param description:
    :param title:
    :param to_user_name:
    :param from_user_name:
    :param media_id:
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
            <Music>
                <Title><![CDATA[%s]]></Title>
                <Description><!CDATA[%s]]></Description>
                <MusicUrl><![CDATA[%s]]></MusicUrl>
                <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
                <ThumbMediaId><![CDATA[%s]]></ThumbMediaId>
            </Music>
            </xml>
    """ % (to_user_name, from_user_name, str(int(now)), msg_type, title, description, music_url, hq_music_url, thumb_media_id)
    return replay


def replay_news(to_user_name, from_user_name, article_count, item):
    """
    回复图文消息
    :param to_user_name:
    :param from_user_name:
    :param create_time:
    :param article_count:
    :param item: list {title, description, pic_url, url}
    :return:
    """
    now = time.time()
    replay = """
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>%s</ArticleCount>
            <Articles>
    """ % (to_user_name, from_user_name, str(int(now)), article_count)
    for index in item:
        tmp = """
            <item>
            <Title><![CDATA[%s]]</Title>
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
            </item>
        """ % (index.get('title'), index.get('description'), index.get('pic_url'), index.get('url'))
        replay += tmp

    replay += """
        </Articles>
        </xml>
    """

    return replay


