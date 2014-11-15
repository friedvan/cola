#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (c) 2013 Qin Xuye <qin@qinxuye.me>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Created on 2013-6-7

@author: Chine
'''

from cola.core.opener import MechanizeOpener
from cola.core.urls import Url, UrlPatterns
from cola.job import Job

from login import WeiboLogin
from parsers import MicroBlogParser, ForwardCommentLikeParser,\
                    UserInfoParser, UserFriendParser
from conf import starts, user_config, instances
from bundle import WeiboUserBundle

import sys
import os
import time
import smtplib
from email.mime.text import MIMEText
import subprocess

SLEEP_TIME=5

mail_host="smtp.163.com"
mail_user="rabbitlee_ok"
mail_pass="564335491"
mail_postfix="163.com"

def login_hook(opener, **kw):
    username = str(kw['username'])
    passwd = str(kw['password'])
    
    loginer = WeiboLogin(opener, username, passwd)
    return loginer.login()

url_patterns = UrlPatterns(
    Url(r'http://weibo.com/aj/mblog/mbloglist.*', 'micro_blog', MicroBlogParser),
    Url(r'http://weibo.com/aj/.+/big.*', 'forward_comment_like', ForwardCommentLikeParser),
    Url(r'http://weibo.com/\d+/info', 'user_info', UserInfoParser),
    Url(r'http://weibo.com/p/\d+/info', 'user_info', UserInfoParser),
    Url(r'http://weibo.com/\d+/follow.*', 'follows', UserFriendParser),
    Url(r'http://weibo.com/\d+/fans.*', 'fans', UserFriendParser)
)

def get_job():
    # print sys.argv[1]
    # starts = load_start(sys.argv[1])
    # print len(starts)
    return Job('sina weibo crawler', url_patterns, MechanizeOpener, starts,
               is_bundle=True, unit_cls=WeiboUserBundle,
               instances=instances, debug=True, user_conf=user_config,
               login_hook=login_hook)

def load_start(src):
    with open(src) as fin:
        return [str(line.strip()) for line in fin]


def send_mail(to_list, sub, content):
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


def autohalt(filename):
    while True:
        ps_string = os.popen('ps -ax | grep '+filename+'|grep -v grep  ', 'r').read()
        ps_strings = ps_string.strip().split('\n')
        if len(ps_strings) < 2:
            mailto_list = ["287535211@qq.com"]
            send_mail(mailto_list, "process stop, restart ", str(time.time()))
            cmds = ['python', '__init__.py']
            subprocess.Popen(cmds)
            # return
        else:
            print 'Still ' + len(ps_strings) + ' Processes, waiting %s min...' % SLEEP_TIME
            time.sleep(60*SLEEP_TIME)

if __name__ == "__main__":
    from cola.worker.loader import load_job
    load_job(os.path.dirname(os.path.abspath(__file__)))
    autohalt()


