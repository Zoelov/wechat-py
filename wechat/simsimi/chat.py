# -*- coding: utf-8 -*-
from django.conf import settings
from utils.public import RequestAPI
import logging

logger = logging.getLogger(__name__)


def chat_sim(msg):
    """
    聊天
    :param msg:
    :return:
    """
    url = settings.SIMSIMI_URL + '?key=%s&lc=zh&ft=1.0&text=%s' % (settings.SIM_KEY, msg)
    logger.info('url=%s' % url)
    try:
        ret = RequestAPI.access_data(url, 'GET')
        logger.info(ret)
        if ret.get('status') == 200:
            if ret.get('data').get('result') == 100:
                logger.info(u'得到回复成功')
                return ret.get('data').get('response')
            else:
                logger.error(u'发生错误，error code:%s' % ret.get('data').get('result'))
                return None
        else:
            logger.error(u'响应失败')
            return None
    except Exception as exc:
        logger.error(u'发生异常，error msg:%s' % exc.message, exc_info=True)
        raise exc
