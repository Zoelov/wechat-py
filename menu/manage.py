# -*- coding:utf-8 -*-

import sys
import os
from os.path import dirname, abspath

reload(sys)
sys.setdefaultencoding('utf-8')
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
import django
import json

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wh.settings")

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()

from django.conf import settings
from utils.public import RequestAPI, access_token
import logging

logger = logging.getLogger('menu.manage')


def create_menu(access_token):
    """
    创建菜单
    :return:
    """
    url = settings.CREATE_MENU_URL + access_token
    logger.info('url=%s' % url)

    param = {
        'button': [
            {
                'name': u"人脸检测",
                'sub_button': [
                    {
                        'type': 'pic_sysphoto',
                        'name': u'系统相机',
                        'key': 'FD',
                        'sub_button': []
                    },
                    {
                        'type': 'pic_photo_or_album',
                        'name': u'相册',
                        'key': 'FD',
                        'sub_button': []
                    }
                ]
            },
            {
                'name': u'人脸识别',
                'sub_button': [
                    {
                        'type': 'pic_sysphoto',
                        'name': u'系统相机',
                        'key': 'FR',
                        'sub_button': []
                    },
                    {
                        'type': 'pic_photo_or_album',
                        'name': u'相册',
                        'key': 'FR',
                        'sub_button': []
                    }
                ]
            },
            {
                'name': u'证件识别',
                'sub_button': [
                    {
                        'type': 'pic_sysphoto',
                        'name': u'系统相机',
                        'key': 'IR',
                        'sub_button': []
                    },
                    {
                        'type': 'pic_photo_or_album',
                        'name': u'相册',
                        'key': 'IR',
                        'sub_button': []
                    }
                ]
            }
        ]
    }

    logger.info('param = %s' % param)
    try:
        ret = RequestAPI.access_data(url, 'POST', json.dumps(param, ensure_ascii=False))
        if ret.get('status') == 200 and ret.get('data').get('errcode') == 0:
            logger.info(u'创建菜单成功')
            return True
        else:
            logger.error(
                u'创建菜单失败，errorcode:%s errmsg:%s' % (ret.get('data').get('errcode'), ret.get('data').get('errmsg')))
            return False
    except Exception as exc:
        logger.error(u'创建菜单发生异常,error msg:%s' % exc.message, exc_info=True)
        raise exc


def delete_menu(access_token):
    """
    删除菜单
    :param access_token:
    :return:
    """
    url = settings.DELETE_MENU_URL + access_token
    logger.info('url=%s' % url)

    try:
        ret = RequestAPI.access_data(url, 'GET')
        if ret.get('status') == 200 and ret.get('data').get('errcode') == 0:
            logger.info(u'删除菜单成功')
            return True
        else:
            logger.error(
                u'删除菜单失败，errorcode:%s errmsg:%s' % (ret.get('data').get('errcode'), ret.get('data').get('errmsg')))
            return False
    except Exception as exc:
        logger.error(u'删除菜单发生异常,error msg:%s' % exc.message, exc_info=True)
        raise exc


if __name__ == '__main__':
    try:
        logger.info(u'开始创建菜单。。。。。')
        token = access_token()
        delete_menu(token)

        ret = create_menu(token)
        if ret:
            logger.info(u'创建菜单成功')
    except Exception as exc:
        logger.error(u'error msg:%s' % exc.message)
