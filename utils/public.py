# -*- coding:utf-8 -*-
import uuid


def create_uuid(name=''):
    '''
    自动生成36位uuid
    :param name:
    :return:
    '''
    return str(uuid.uuid1())