# -*- coding:utf-8 -*-
from django.db import models
import logging
import time
from utils import public

logger = logging.getLogger(__name__)


class RecManager(models.Manager):
    def add_msg(self, from_user, msg_type,
                create_time, msg_id, msg_content=None, pic_url=None, media_id=None,
                format=None, recognition=None, thumb_media_id=None, location_x=None, location_y=None,
                scale=None, label=None, title=None, description=None, url=None, is_reply=0
                ):
        """
        插入收到的消息
        :param is_reply:
        :param from_user:
        :param msg_type:
        :param create_time:
        :param msg_content:
        :param msg_id:
        :param pic_url:
        :param media_id:
        :param format:
        :param recognition:
        :param thumb_media_id:
        :param location_x:
        :param location_y:
        :param scale:
        :param label:
        :param title:
        :param description:
        :param url:
        :return:
        """
        try:
            time_arry = time.localtime(float(create_time))
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_arry)
            obj = self.model(
                id=public.create_uuid('msg'),
                from_user_id=from_user,
                msg_type=msg_type,
                create_time=time_str,
                msg_content=msg_content,
                msg_id=msg_id,
                pic_url=pic_url,
                media_id=media_id,
                format=format,
                recognition=recognition,
                thumb_media_id=thumb_media_id,
                location_x=location_x,
                location_y=location_y,
                scale=scale,
                label=label,
                title=title,
                description=description,
                url=url,
                is_reply=is_reply
            )
            obj.save()
            logger.info(u'保存收到的消息成功')
            return obj
        except Exception as exc:
            logger.error(u'保存信息发生异常，error msg:%s' % exc.message, exc_info=True)
            raise exc

    def update_status(self, obj, is_reply):
        """
        更新消息回复状态
        :param obj:
        :param is_reply:
        :return:
        """
        try:
            obj.is_reply = is_reply
        except Exception as exc:
            logger.error(u'更新消息状态发生异常，error msg:%s' % exc.message, exc_info=True)
            raise exc


class RepManager(models.Manager):
    def add_msg(self, rec_id, to_user_id, msg_type, create_time,
                msg_content, media_id=None, title=None, description=None,
                music_url=None, hq_music_url=None, thumb_media_id=None,
                article_count=None, articles=None, pic_url=None, url=None):
        """
        保存回复的消息
        :param rec_id:
        :param to_user_id:
        :param msg_type:
        :param create_time:
        :param msg_content:
        :param media_id:
        :param title:
        :param description:
        :param music_url:
        :param hq_music_url:
        :param thumb_media_id:
        :param article_count:
        :param articles:
        :param pic_url:
        :param url:
        :return:
        """
        try:
            time_arry = time.localtime(float(create_time))
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_arry)
            obj = self.model(
                rec=rec_id,
                to_user=to_user_id,
                msg_type=msg_type,
                create_time=time_str,
                msg_content=msg_content,
                media_id=media_id,
                title=title,
                description=description,
                music_url=music_url,
                hq_music_url=hq_music_url,
                thumb_media_id=thumb_media_id,
                article_count=article_count,
                articles=articles,
                pic_url=pic_url,
                url=url
            )
            obj.save()
            logger.info(u'保存回复消息成功')
        except Exception as exc:
            logger.error(u'保存回复消息发生异常，error msg:%s' % exc.message, exc_info=True)
            raise exc
