# -*- coding:utf-8 -*-
from django.db import models
import logging
import datetime
import time


logger = logging.getLogger(__name__)


class UsersManager(models.Manager):
    def add_user(self, open_id, subscribe, nickname, sex, city, country, province, language, headimgurl, subscribe_time, unionid, remark, groupid):
        """
        """
        try:
            time_arry = time.localtime(float(subscribe_time))
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_arry)
            user = self.model(
                open_id=open_id,
                subscribe=subscribe,
                nickname=nickname,
                sex=sex,
                city=city,
                country=country,
                province=province,
                language=language,
                headimgurl=headimgurl,
                subscribe_time=time_str,
                unionid=unionid,
                remark=remark,
                groupid=groupid
            )
            user.save()
        except Exception as exc:
            logger.error(u'插入用户信息发生异常, error msg:%s' % exc.message, exc_info=True)
            raise exc


class AccessManager(models.Manager):
    def add_token(self, access_token, expires, create_time, end_time, is_valid=1):
        """
        插入token信息
        :param create_time:
        :param access_token:
        :param expires:
        :param end_time:
        :param is_valid:
        :return:
        """
        try:
            obj = self.model(
                access_token=access_token,
                expires_time=expires,
                create_time=create_time.strftime('%Y-%m-%d %H:%M:%S'),
                end_time=end_time,
                is_valid=is_valid
            )
            obj.save()
        except Exception as exc:
            logger.error(u'保存token信息失败, error msg:%s' % exc.message, exc_info=True)
            raise exc

    def set_invalid(self):
        """
        置invalid
        :return:
        """
        try:
            obj = self.filter(is_valid=1)
            if obj.exists():
                logger.info(u'查询到valid的token')
                for index in obj:
                    index.is_valid = 0
                    index.save()
        except Exception as exc:
            logger.error(u'置invalid发生异常，error msg:%s' % exc.message, exc_info=True)
            raise exc

