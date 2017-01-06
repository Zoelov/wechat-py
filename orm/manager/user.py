# -*- coding:utf-8 -*-
from django.db import  models
import logging


logger = logging.getLogger(__name__)


class OpenInfoManager(models.Manager):
    def add_open_id(self, id, total, count, next_openid):
        """
        保存open id信息
        :param id:
        :param total:
        :param count:
        :param next_openid:
        :return:
        """
        logger.info('id = %s tota=%s count=%s next_openid=%s' %
                    (id, total, count, next_openid))
        try:

            obj = self.model(
                id=id,
                total=total,
                count=count,
                next_openid=next_openid
            )
            obj.save()
        except Exception as exc:
            logger.error(u'插入数据发生异常，error msg:%s' % exc.message, exc_info=True)
            raise exc


