# -*- coding:utf-8 -*-
from django.db import models
import logging
import datetime
import time


logger = logging.getLogger(__name__)


class UsersManager(models.Manager):
    def add_user(self, open_id, subscribe, nickname, sex, city, country, province, language, headimgurl, subscribe_time, unionid, remark, groupid, unsubscribe_time=None):
        """
        """
        try:
            time_arry = time.localtime(float(subscribe_time))
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_arry)
            user = self.model(
                id=open_id,
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
                groupid=groupid,
                unsubscribe_time=unsubscribe_time
            )
            user.save()
            return user.nickname
        except Exception as exc:
            logger.error(u'插入用户信息发生异常, error msg:%s' % exc.message, exc_info=True)
            raise exc

    def update_info(self, user_dict):
        """
        更新用户信息
        :param user_dict:
        :return:
        """
        try:
            obj = self.filter(id=user_dict.get('openid'))
            if obj.exists():
                obj = obj[0]
                if 'subscribe' in user_dict:
                    obj.subscribe = user_dict.get('subscribe')
                if 'nickname' in user_dict:
                    obj.nickname = user_dict.get('nickname')
                if 'sex' in user_dict:
                    obj.sex = user_dict.get('sex')
                if 'city' in user_dict:
                    obj.city = user_dict.get('city')
                if 'country' in user_dict:
                    obj.country = user_dict.get('country')
                if 'province' in user_dict:
                    obj.province = user_dict.get('province')
                if 'language' in user_dict:
                    obj.language = user_dict.get('language')
                if 'headimgurl' in user_dict:
                    obj.headimgurl = user_dict.get('headimgurl')
                if 'subscribe_time' in user_dict:
                    time_arry = time.localtime(float(user_dict.get('subscribe_time')))
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_arry)
                    obj.subscribe_time = time_str
                if 'unionid' in user_dict:
                    obj.unionid = user_dict.get('unionid')
                if 'remark' in user_dict:
                    obj.remark = user_dict.get('remark')
                if 'groupid' in user_dict:
                    obj.groupid = user_dict.get('groupid')
                if 'unsubscribe_time' in user_dict:
                    obj.unsubscribe_time = user_dict.get('unsubscribe_time')
                obj.save()
                return obj.nickname
        except Exception as exc:
            logger.error(u'更新用户信息发生异常，error msg:%s' % exc.message, exc_info=True)
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


class LocationManager(models.Manager):
    def add_location(self, from_user_name, create_time, latitude, longitude, precision):
        """

        :param from_user_name:
        :param create_time:
        :param latitude:
        :param longitude:
        :param precision:
        :return:
        """
        try:
            time_arry = time.localtime(float(create_time))
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_arry)
            obj = self.model(
                user=from_user_name,
                create_time=time_str,
                latitude=latitude,
                longitude=longitude,
                precision=precision
            )
            obj.save()
            logger.info(u'保存用户地理位置信息成功user=%s' % from_user_name)
        except Exception as exc:
            logger.error(u'保存用户地理位置信息发生异常，error msg:%s' % exc.message, exc_info=True)
            raise exc

