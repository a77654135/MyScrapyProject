# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from MyScrapyProject.items.items import XicidailiItem

class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/']
    base_url = r'http://www.xicidaili.com/nn/'

    custom_settings = {
        'REDIS_SCHEDULER_KEY': 'xicidaili:scheduler_queue_key',
        'REDIS_DUPEFILTER_KEY': 'xicidaili:dupefilter_key',
        'SCHEDULER_QUEUE': 'MyScrapyProject.core.queue.RedisQueue',
        'DOWNLOAD_DELAY':10,
        'ITEM_PIPELINES': {
            'MyScrapyProject.pipelines.XicidailiPipelines.XicidailiMongodbPipeline': 300,
        }
    }


    def parse(self, response):
        self.getDetailPage(response)
        pageCount = response.xpath('//div[@class="pagination"]/a[last()-1]/text()').extract_first()
        pageCount = int(pageCount)
        for i in range(2,pageCount + 1):
            url = "{}{}".format(self.base_url,i)
            yield Request(url,callback=self.getDetailPage)


    def getDetailPage(self,response):
        rows = response.xpath('//table[@id="ip_list"]//tr')
        if len(rows) > 1:
            rows = rows[1:]
        for r in rows:
            item = XicidailiItem()
            item["ip"] = r.xpath('td[2]/text()').extract_first()
            item["port"] = r.xpath('td[3]/text()').extract_first()
            item["address"] = r.xpath('td[4]/a/text()').extract_first()
            item["isAnonymous"] = r.xpath('td[5]/text()').extract_first()
            item["type"] = r.xpath('td[6]/text()').extract_first()
            item["speed"] = r.xpath('td[7]/div/@title').extract_first()
            item["connectTime"] = r.xpath('td[8]/div/@title').extract_first()
            item["survivalTime"] = r.xpath('td[9]/text()').extract_first()
            item["verifyTime"] = r.xpath('td[10]/text()').extract_first()
            yield item


