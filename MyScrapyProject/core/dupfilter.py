from __future__ import print_function
import os
import logging
import redis

from scrapy.utils.request import request_fingerprint
from scrapy.dupefilters import BaseDupeFilter

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_DUPEFILTER_KEY = 'dupefilter_key'

class RedisDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, server, key, debug=False):
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings, SPIDER_NAME):
        debug = settings.getbool('DUPEFILTER_DEBUG')
        host = settings.get('REDIS_HOST',REDIS_HOST)
        port = settings.get('REDIS_PORT',REDIS_PORT)
        db = settings.get('REDIS_DB',REDIS_DB)
        key = settings.get('REDIS_DUPEFILTER_KEY',REDIS_DUPEFILTER_KEY)
        key = "{}:{}".format(SPIDER_NAME,key)
        server = redis.Redis(host=host,port=port,db=db)
        return cls(server,key, debug)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if self.server.sismember(self.key,fp):
            return True
        self.server.sadd(self.key,fp)
        return False

    def request_fingerprint(self, request):
        return request_fingerprint(request)

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
