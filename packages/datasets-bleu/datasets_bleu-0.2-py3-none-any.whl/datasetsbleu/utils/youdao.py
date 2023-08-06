#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/8/17 17:01
# @Author  : zhangzhenhua@wps.cn
# @File    : youdao.py

import sys
from os.path import dirname, abspath

path = dirname(dirname(dirname(dirname(abspath(__file__)))))
sys.path.append(path)


import requests
import time
import random
import hashlib
import tenacity
import urllib3

from faker import Factory
from urllib.parse import urlencode

urllib3.disable_warnings()

PROXY_DICT_3 = {
    'proxyHost': 'u3125.5.tn.16yun.cn',  # 代理服务器
    'proxyPort': '6441',
    'proxyUser': '16OLSEPY',  # 代理验证信息
    'proxyPass': '172158'
}


class YoudaoFanyi(object):
    """
    有道翻译接口
    """

    def __init__(self, input, output, proxy=None):
        self.sess = requests.session()
        self.input = input
        self.output = output
        self.base_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.proxy = proxy
        self.user_agent = Factory.create().user_agent()
        self.formdate = {
            'i': '',
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': '15970401634701',
            'sign': '76ff47ba12e757d1c0f7fe05c5508af2',
            'lts': '1597040163470',
            'bv': 'aa510f0fd141e8aee98da89f3b8bad73',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }
        self.headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': self.user_agent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://fanyi.youdao.com/',
            'Origin': 'http://fanyi.youdao.com',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.load_message()

    def load_message(self):
        """
        加载页面,获取session
        :return:
        """
        url = 'http://fanyi.youdao.com'
        self.formdate['bv'] = self.get_bv()
        while True:
            try:
                self.sess.get(url, headers=self.headers, timeout=15, proxies=self.fetch_one_proxy())
                now_time = int(time.time() * 1e3) - 30
                self.sess.cookies.set('___rl__test__cookies',str(now_time))
                self.sess.cookies.set('OUTFOX_SEARCH_USER_ID_NCOO','undefined')
                break
            except Exception as e:
                continue

    def get_formdate(self, text):
        """
        构造post请求的formdata
        :return:
        """
        self.formdate['from'] = self.input
        self.formdate['to'] = self.output
        now_time = int(time.time() * 1e3)
        self.formdate['lts'] = str(now_time)
        self.formdate['salt'] = str(now_time) + str(random.randint(0, 9))
        self.formdate['i'] = text
        self.formdate['sign'] = self.get_sign(text, self.formdate['salt'])

    def get_bv(self):
        """
        生成bv
        :return:
        """
        return self.md5(self.user_agent)

    def get_sign(self, text, salt):
        """
        根据传入的文本和加的盐构造signature
        :param text:
        :param salt:
        :return:
        """
        sign = self.md5('fanyideskweb' + text + salt + 'Tbh5E8=q6U3EXe+&L[4c@')
        return sign

    def md5(self, keyword):
        """
        生成MD5
        :param keyword: 输入文本
        :return:输出md5值
        """
        h = hashlib.md5()
        h.update(keyword.encode('utf-8'))
        sign = h.hexdigest()
        return sign

    def parse_response(self, res, text):
        """
        解析响应对象
        :param res: 响应对象
        :return:
        """
        zh_list = list()
        en_list = list()
        src_tgt = list()
        for _ in res.json()['translateResult']:
            tgt_list = list()
            src_list = list()
            for i in _:
                if i['tgt']:
                    src_list.append(i['src'])
                    tgt_list.append(i['tgt'])
                    item = {
                        'src':i['src'],
                        'dst':i['tgt']
                    }
                    src_tgt.append(item)
            zh = ''.join(tgt_list)
            zh_list.append(zh)
            en_list.append(''.join(src_list))

        item = {
            'src': '\n'.join(en_list),
            'tgt': '\n'.join(zh_list).strip(),
            'youdao_trans': src_tgt,
        }
        return item

    @tenacity.retry(stop=tenacity.stop_after_attempt(5))
    def req_post_three(self, session, url, param=None, headers=None, data=None, proxy=None):
        """
        封装post请求，重试5次
        :param url: 目标网站url
        :param param: 请求参数
        :param headers: 请求头
        :param data: 请求体
        :param proxy: 是否加入代理
        :return:响应对象
        """
        if proxy:
            res = session.post(url, params=param, headers=headers, data=data, verify=False, timeout=10,
                               proxies=self.fetch_one_proxy())
        else:
            res = session.post(url, params=param, headers=headers, data=data, verify=False, timeout=10)
        return res

    def fetch_one_proxy(self):
        """
        提取一个代理
        :return: 构造一个proxies
        """
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": PROXY_DICT_3.get('proxyHost', None),
            "port": PROXY_DICT_3.get('proxyPort', None),
            "user": PROXY_DICT_3.get('proxyUser', None),
            "pass": PROXY_DICT_3.get('proxyPass', None),
        }
        # 设置 http和https访问都是用HTTP代理
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies

    def run(self, text):
        """
        执行函数
        :return:
        """
        self.get_formdate(text)
        payload = urlencode(self.formdate)
        res = self.req_post_three(session=self.sess, url=self.base_url, headers=self.headers, data=payload,
                                  proxy=self.proxy)
        item = self.parse_response(res, text)
        return item


class YoudaoFanyiApi():
    # en - en  zh - zh-CHS
    def __init__(self, input, output, proxy=None):
        self.input = input
        self.output = output
        self.proxy = proxy
        self.youdao = YoudaoFanyi(self.input, self.output, proxy=self.proxy)

    def get_obj(self):
        self.youdao = YoudaoFanyi(self.input, self.output, proxy=self.proxy)

    @tenacity.retry(stop=tenacity.stop_after_attempt(5))
    def trans(self, text):
        try:
            zh = self.youdao.run(text)
            return zh
        except:
            self.get_obj()



if __name__ == '__main__':

    youdao = YoudaoFanyiApi(input='zh-CHS', output='en', proxy=0)
    # while True:
    zh = youdao.run("第六届次区域经济合作河内峰会是次区域合作的一次重要活动。")
    #     time.sleep(1.0)
    print(zh)
    pass
