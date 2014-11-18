__author__ = 'pzc'

import os
import sys
import time
import smtplib
import socket
from email.mime.text import MIMEText
import subprocess

SLEEP_TIME = 5

mail_host = "smtp.163.com"
mail_user = "rabbitlee_ok"
mail_pass = "564335491"
mail_postfix = "163.com"


def send_mail(to_list, sub, content):
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


def get_my_ip():
    """
    Returns the actual ip of the local machine.

    This code figures out what source address would be used if some traffic
    were to be sent out to some well known address on the Internet. In this
    case, a Google DNS server is used, but the specific address does not
    matter much.  No traffic is actually sent.
    """
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"


if __name__ == '__main__':
    count = 0
    restart = 0
    p = subprocess.Popen(['python', '__init__.py'], stdout=sys.stdout, stdin=sys.stdin, stderr=sys.stderr)
    while True:
        code = p.poll()
        if code is None:
            count += 1
            print 'still running %s' % count
        else:
            restart += 1
            print 'finish with code %s, restarting' % code
            p = subprocess.Popen(['python', '__init__.py'], stdout=sys.stdout, stdin=sys.stdin, stderr=sys.stderr)
            send_mail(
                ['287535211@qq.com'],
                "error crawling weibo",
                "ip: %s\nnumber: %s\nrestart: %s\n" % (get_my_ip(), restart, time.strftime('%Y-%m-%d',time.localtime(time.time())))
            )
        time.sleep(60 * SLEEP_TIME)
