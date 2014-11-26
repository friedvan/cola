__author__ = 'pzc'


import redis
import sys

REDIS_HOST = 'localhost'


if '__name__' == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python set_start_uid.py weibo_uid'
        sys.exit(0)
    rds = redis.Redis(host=REDIS_HOST)
    start_uid = sys.argv[1]
    try:
        int(start_uid)
        rds.rpush('cola:uids', start_uid)
    except:
        print 'usage: python set_start_uid.py weibo_uid'
        sys.exit(0)

    print 'success!'