#coding:utf-8
import scrapy
from scrapy.http import Request,Response
from bs4 import BeautifulSoup
import re
import logging
from MyScrapyProject.items import items


class Xuexi111Spider(scrapy.Spider):
    name = "xuexi111"
    allowed_domains = ["xuexi111.com"]
    start_urls = ['http://www.xuexi111.com/']

    custom_settings = {
        'REDIS_SCHEDULER_KEY':'xuexi111:scheduler_queue_key',
        'REDIS_DUPEFILTER_KEY':'xuexi111:dupefilter_key',
        'MONGODB_COLLECTION':'xuexi111',
        'SCHEDULER_QUEUE': 'MyScrapyProject.core.queue.RedisQueue',
        'ITEM_PIPELINES': {
            'MyScrapyProject.pipelines.Xuexi111Pipelines.DropInvalidItem': 200,
            'MyScrapyProject.pipelines.Xuexi111Pipelines.MongodbPipeline': 300,
        }
    }

    def parse(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        a_list = html.select('#dibudao > a')
        link_list = []
        for a in a_list:
            try:
                link_list.append(a['href'])
            except:
                continue
        a_nav_list = html.select('.nav a')[1:]
        for a in a_nav_list:
            try:
                link_list.append(a['href'])
            except:
                continue

        for link in link_list:
            yield Request(link,callback=self._get_page_list)

    def _get_page_list(self,response):
        self._get_detail_page(response)
        try:
            html = BeautifulSoup(response.text, 'lxml')
            show_page = html.select('.show-page a')
            href = show_page[-1]['href']
            count_str = re.findall(r'.*?_(\d+)\.html', href)[0]
            count = int(count_str)
        except:
            self.log("_get_page_list  error  ,url:  {}".format(response.url),level=logging.WARNING)
        else:
            for i in range(2, count + 1):
                c = re.sub(r'\d+\.html', "{}.html".format(i), href, count=1)
                yield Request(c,callback=self._get_detail_page)

    def _get_detail_page(self,response):
        crawl_list = []
        try:
            html = BeautifulSoup(response.text, 'lxml')
            table_list = html.select('table.list a')
            if table_list:
                for a in table_list:
                    try:
                        if re.match(r'^http', a['href']):
                            crawl_list.append(a['href'])
                    except:
                        continue

            topic_list = html.select('div.topic-list li > a')
            if topic_list:
                for a in topic_list:
                    try:
                        if re.match(r'^http', a['href']):
                            crawl_list.append(a['href'])
                    except:
                        continue
        except:
            self.log("_get_detail_page  error  ,url:  {}".format(response.url),level=logging.ERROR)

        for link in crawl_list:
            yield Request(link,callback=self._get_book_page)

    def _get_book_page(self,response):
        item_list = []
        try:
            html = BeautifulSoup(response.text, 'lxml')
            download_list = html.select('table.download-table tr')
            now_list = html.select('div.now a')
            mainCategory = ''
            detailCategory = ''
            try:
                if now_list and len(now_list) > 1:
                    length = len(now_list)
                    if length == 2:
                        mainCategory = now_list[-1].string.strip()
                        detailCategory = now_list[-1].string.strip()
                    else:
                        mainCategory = now_list[-2].string.strip()
                        detailCategory = now_list[-1].string.strip()
            except:
                pass
            for tr in download_list:
                a_list = tr.select('a')
                if a_list:
                    item = items.Xuexi111Item()
                    item_list.append(item)
                    item['originalUrl'] = response.url
                    item['mainCategory'] = mainCategory
                    item['detailCategory'] = detailCategory
                    item['downloadLink'] = ""
                    item['thunderDownloadLink'] = ""
                    for a in a_list:
                        try:
                            href = a['href'].strip()
                            if re.match(r'ed2k', href):
                                item['downloadLink'] = href
                            elif re.match(r'http://lixian', href):
                                item['thunderDownloadLink'] = href
                            else:
                                item['downloadLink'] = href
                            a_string = a.string
                            if a_string:
                                item['bookName'] = a_string.strip()
                        except:
                            continue
            #print response
        except Exception,e:
            self.log("_get_book_page  error:  {}  ,url:  {}".format(e.message,response.url),level=logging.ERROR)
        for item in item_list:
            yield item