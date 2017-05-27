#-.-coding:utf-8

try:
    import cPickle as pickle
except ImportError:
    import pickle

import redis
from scrapy.utils.reqser import request_to_dict,request_from_dict

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_SCHEDULER_KEY = 'scheduler_queue_key'

class BaseQueue(object):
    def __init__(self, server, key):
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings, SPIDER_NAME):
        host = settings.get('REDIS_HOST', REDIS_HOST)
        port = settings.get('REDIS_PORT', REDIS_PORT)
        db = settings.get('REDIS_DB', REDIS_DB)
        key = settings.get('REDIS_SCHEDULER_KEY', REDIS_SCHEDULER_KEY)
        key = "{}:{}".format(SPIDER_NAME, key)
        server = redis.Redis(host=host, port=port, db=db)
        return cls(server, key)

    def close(self):
        self.server.bgsave()
        self.server.bgrewriteaof()

    def push(self, request, spider):
        pass

    def pop(self, spider):
        pass

    def clear(self):
        pass

    @property
    def length(self):
        pass

class RedisQueue(BaseQueue):
    def push(self,request,spider):
        self.server.lpush(self.key,pickle.dumps(request_to_dict(request,spider)))

    def pop(self,spider):
        data = self.server.rpop(self.key)
        if data:
            return request_from_dict(pickle.loads(data),spider)

    def clear(self):
        self.server.delete(self.key)

    @property
    def length(self):
        return self.server.llen(self.key)


class RedisStack(BaseQueue):
    def push(self,request,spider):
        self.server.lpush(self.key,pickle.dumps(request_to_dict(request,spider)))

    def pop(self,spider):
        data = self.server.lpop(self.key)
        if data:
            return request_from_dict(pickle.loads(data),spider)

    def clear(self):
        self.server.delete(self.key)

    @property
    def length(self):
        return self.server.llen(self.key)