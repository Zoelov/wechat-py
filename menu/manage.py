# -*- coding:utf-8 -*-
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
                'name': '人脸检测',
                'sub_button': [
                    {
                        'type': 'pic_sysphoto',
                        'name': '系统拍照',
                        'key': 'pic_sysphoto',
                        'sub_button': []
                    },
                    {
                        'type': 'pic_photo_or_album',
                        'name': '拍照或者从相册',
                        'key': 'pic_photo_or_album',
                        'sub_button': []
                    }
                ]
            },
            {
                'name': '人脸识别',
                'sub_button': [
                    {
                        'type': 'pic_sysphoto',
                        'name': '系统拍照',
                        'key': 'pic_sysphoto',
                        'sub_button': []
                    },
                    {
                        'type': 'pic_photo_or_album',
                        'name': '拍照或者从相册',
                        'key': 'pic_photo_or_album',
                        'sub_button': []
                    }
                ]
            },
            {
                'name': '证件识别',
                'sub_button': [
                    {
                        'type': 'pic_sysphoto',
                        'name': '系统拍照',
                        'key': 'pic_sysphoto',
                        'sub_button': []
                    },
                    {
                        'type': 'pic_photo_or_album',
                        'name': '拍照或者从相册',
                        'key': 'pic_photo_or_album',
                        'sub_button': []
                    }
                ]
            }
        ]
    }

    logger.info('param = %s' % param)
    try:
        ret = RequestAPI.access_data(url, 'POST', param)
        if ret.get('status') == 200 and ret.get('data').get('errcode') == 0:
            logger.info(u'创建菜单成功')
            return True
        else:
            logger.error(u'创建菜单失败，errorcode:%s errmsg:%s' % (ret.get('data').get('errcode'), ret.get('data').get('errmsg')))
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
            logger.error(u'删除菜单失败，errorcode:%s errmsg:%s' % (ret.get('data').get('errcode'), ret.get('data').get('errmsg')))
            return False
    except Exception as exc:
        logger.error(u'删除菜单发生异常,error msg:%s' % exc.message, exc_info=True)
        raise exc


if __name__ == '__main__':
    try:
        logger.info(u'开始创建菜单。。。。。')
        token = access_token()
        delete_menu(token)

        create_menu(token)
    except Exception as exc:
        logger.error(u'error msg:%s' % exc.message)




