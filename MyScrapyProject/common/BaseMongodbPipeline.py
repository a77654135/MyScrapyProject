#-.-coding:utf-8

import pymongo
import logging
import json
from pymongo.errors import PyMongoError

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'scrapyData'

class BaseMongodbPipeline(object):
    def __init__(self,db,coll,useMongo):
        self.db = db
        self.coll = coll
        self.useMongo = useMongo
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        host = settings.get('MONGODB_HOST', MONGODB_HOST)
        port = settings.get('MONGODB_PORT', MONGODB_PORT)
        database = settings.get('MONGODB_DATABASE', MONGODB_DATABASE)
        coll = settings.get('MONGODB_COLLECTION', crawler.spider.name)
        try:
            conn = pymongo.MongoClient(host, port)
            db = conn[database]
            useMongo = True
        except Exception, e:
            useMongo = False
            db = None
            print 'connection mongodb error:  %s' % e.message
        return cls(db, coll, useMongo)

    def data(self,item):
        return json.dumps(item)

    def process_item(self, item, spider):
        if not self.useMongo:
            return item
        try:
            self.db[self.coll].insert(self.data(item))
        except PyMongoError,e:
            self.logger.log(logging.ERROR,
                            r"{}: mongodbPipeline_error: insert into database error.____{}____  url:  {}".format(
                                spider.name, e.message, item['originalUrl']))
        finally:
            return item
