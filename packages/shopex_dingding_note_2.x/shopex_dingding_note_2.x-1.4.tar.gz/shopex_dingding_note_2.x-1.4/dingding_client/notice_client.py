# -*- coding: utf-8 -*-
import time
import random
import threading
from gevent.queue import JoinableQueue


from inner_lib.func_ext import get_md5, http_request, message_format, singleton
from conf.config import MAXSIZE


@singleton
class NoticeClient(object):
    init_flag = False

    def __init__(self, app_key, app_secret, api_url):
        if not self.init_flag:  # 防止重复执行init方法
            self.api_url = api_url
            self.app_key = app_key
            self.app_secret = app_secret
            self.req_q = JoinableQueue(MAXSIZE)
            self.init_flag = True
            t1 = threading.Thread(target=http_request, args=[self.api_url, self.req_q])
            t1.start()
        else:
            return

    def sys_params(self, body):
        """构造请求参数参数"""
        time.sleep(1)
        now = int(time.time())
        auth_key = '%d-%s-%s' % (now, self.app_secret, self.app_key)
        auth_key_md5 = get_md5(auth_key)
        auth_str = auth_key_md5[0:4] + str(random.randint(100, 999)) + auth_key_md5[4:24] + str(
            random.randint(10000, 99999)) + auth_key_md5[24:]
        _params = {
            "key": self.app_key,
            "auth_str": auth_str,
            "timestamp": now,
            "req_msg": body,
        }
        return _params

    def send(self, data, to_users):
        to_users = "|".join(to_users)
        data = message_format(data)
        body = {
            "to_user": to_users,
            "content": data
        }
        _params = self.sys_params(body)
        self.req_q.put(_params)

        return True


if __name__ == '__main__':
    pass