# -*- coding:utf-8 -*-
from django.db import models
import logging
import time


logger = logging.getLogger(__name__)


class MenuManager(models.Manager):
    def add_event(self, user_id, create_time, event_type, event_key, pic_count, is_valid=1):
        """
        保存菜单事件消息
        :param is_valid:
        :param user_id:
        :param create_time:
        :param event_type:
        :param event_key:
        :param pic_count:
        :return:
        """
        try:
            time_arry = time.localtime(float(create_time))
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_arry)
            obj = self.model(
                user_id=user_id,
                create_time=time_str,
                event_key=event_key,
                event_type=event_type,
                pic_count=pic_count,
                is_valid=is_valid
            )
            obj.save()
            return obj
        except Exception as exc:
            logger.error(u'保存菜单事件消息发生异常，error msg:%s' % exc.message, exc_info=True)
            raise exc