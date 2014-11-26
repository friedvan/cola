__author__ = 'pzc'


import redis
import json

REDIS_HOST = '112.124.4.10'

def load_accounts_from_csv(fname):
    accounts = []
    for line in open(fname):
        username, password = line.rstrip().split(',')
        accounts.append({"username": username, "password": password})
    return accounts


if '__name__' == '__main__':
    rds = redis.Redis(host=REDIS_HOST)
    accounts = load_accounts_from_csv('weibo_accounts.csv')
    for act in accounts:
        rds.rpush('cola:account', json.dumps(act))
    print 'success!'