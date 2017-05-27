#-.-coding:utf-8
from scrapy.utils.misc import load_object

class Scheduler(object):

    def __init__(self, queue, logunser=False, stats=None, dupefilter=None):
        self.df = dupefilter
        self.logunser = logunser
        self.stats = stats
        self.queue = queue

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_settings(settings,crawler.spidercls.name)
        pqclass = load_object(settings['SCHEDULER_QUEUE'])
        queue = pqclass.from_settings(settings,crawler.spidercls.name)
        logunser = settings.getbool('LOG_UNSERIALIZABLE_REQUESTS', settings.getbool('SCHEDULER_DEBUG'))

        return cls(queue,logunser,crawler.stats,dupefilter)

    def has_pending_requests(self):
        return self.queue.length

    def open(self, spider):
        self.spider = spider
        return self.df.open()

    def close(self, reason):
        self.queue.close()
        return self.df.close(reason)

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        self.queue.push(request,self.spider)
        self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        return True

    def next_request(self):
        request = self.queue.pop(self.spider)
        if request:
            self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
        return request



