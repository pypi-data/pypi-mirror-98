# -*- coding: UTF-8 -*-
from __future__ import with_statement
import time
import urllib2
import hashlib
import socket
socket.setdefaulttimeout(15)
import threading
import json

from conf.config import RETRY_COUNT, TIME_STEP
from inner_lib.log import *


def get_md5(string):
    try:
        m = hashlib.md5()
        m.update(string)
        dest = m.hexdigest()
        return dest
    except:
        return False


def http_request(url, req_q, headers={'user-agent': 'shopex/spider'}):
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    retry_count = RETRY_COUNT
    '''
        数据请求处理
    '''
    while 1:
        try:
            data = json.dumps(req_q.get(block=False))
        except Exception, e:
            time.sleep(2)
            continue
        while retry_count >= 0:
            try:
                request = urllib2.Request(url=url, headers=headers, data=data)
                response = opener.open(request).read()
                response = json.loads(response)
                status = response.get("errmsg")
            except Exception, e:
                response = e
                status = 'fail'
                logger.error(e)

            if status != "ok":  # 尝试重发
                logger.error(response)
                retry_count -= 1
                continue
            else:
                time.sleep(TIME_STEP)
                break


def message_format(data):
    event_time = time.strftime("%Y-%m-%d %H:%M:%S", data.get("timestamp", time.localtime()))
    event_main = data.get("main", "")
    event_service = data.get("service", "")
    event_message = data.get("message", "")
    return "事件产生时间:%s  事件产生主体:%s  所属服务:%s  事件内容:%s" % (event_time, event_main, event_service, event_message)


def singleton(cls):
    _instance = {}
    _instance_lock = threading.Lock()

    def wrappers(*args, **kwargs):
        # 双重检查锁定创建单例
        if not _instance.get(cls.__name__):
            with _instance_lock:
                if not _instance.get(cls.__name__):
                    _instance[cls.__name__] = cls(*args, **kwargs)
                    return _instance[cls.__name__]
        else:
            return _instance.get(cls.__name__)

    return wrappers