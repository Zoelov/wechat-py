# -*- coding:utf-8 -*-
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wh.settings")

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()
from django.conf import settings
from service.user import get_access_token, get_open_id, get_users
import logging
from orm import models as orm_models
from time import sleep

logger = logging.getLogger(__name__)


class Task(object):
    def __init__(self):
        self.app_id = settings.USER_APP_ID
        self.app_secret = settings.USER_APP_SECRET
        self.next_openid = None
        self.total = 0  # 关注公众号的总人数
        self.access_token = None
        self.expires = None
        self.count = 0  # 此次拉去的openid的个数

    def save_users(self):
        """
        """
        try:
            token = get_access_token(self.app_id, self.app_secret)
            if token:
                logger.info(u'获取access_token成功')
                self.access_token = token.get('access_token')
                self.expires = token.get('expires_in')

                open = get_open_id(self.access_token, self.next_openid)
                if open:
                    logger.info(u'获取openid list成功')
                    self.total = open.get('total')
                    self.count = open.get('count')
                    self.next_openid = open.get('next_openid')

                    open_id_list = open.get('data')
                    for index in open_id_list:
                        user_obj = orm_models.User.objects.filter(open_id=index)
                        if user_obj.exists():
                            logger.info(u'此open_id已经存在，open_id=%s' % index)
                            continue
                        users = get_users(self.access_token, index)
                        if users:
                            logger.info('users=%s' % users)
                            orm_models.User.object.add_user(
                                users.get('openid'),
                                users.get('subscribe'),
                                users.get('nickname'),
                                users.get('sex'),
                                users.get('city'),
                                users.get('country'),
                                users.get('province'),
                                users.get('language'),
                                users.get('headimgurl'),
                                users.get('subscribe_time'),
                                users.get('unionid'),
                                users.get('remark'),
                                users.get('groupid')

                            )
        except Exception as exc:
            logger.error(u'获取用户信息发生异常，error msg:%s' % exc.message, exc_info=True)
            raise exc

    def run(self):
        expire = self.expires
        logger.info(u'过期时间为:%s秒' % expire)

        while True:
            try:
                self.save_users()
                sleep(expire)
            except Exception as exc:
                logger.error(u'发生异常')
                continue

if __name__ == '__main__':
    task = Task()
    task.run()
