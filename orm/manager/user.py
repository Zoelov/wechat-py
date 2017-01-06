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
