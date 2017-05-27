# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request

class KekenetSpider(scrapy.Spider):
    name = 'kekenet'
    allowed_domains = ['kekenet.com']
    start_urls = ['http://www.kekenet.com//soft/']

    base_url = r'http://www.kekenet.com'

    def parse(self, response):
        a_list = response.xpath('//div[@class="box_nav"]//li/a')
        for a in a_list:
            href = a.xpath('@href').extract_first()
            category = a.xpath('text()').extract_first()
            meta = {}
            meta['category'] = category
            return Request('{}{}'.format(self.base_url,href),callback=self.getPageList,meta=meta)

    def getPageList(self,response):
        self.getContentPage(response)
        # meta = response.request.meta.copy()
        # pageList = response.xpath('//div[@class="page th"]/a/@href').extract()
        # for p in pageList:
        #     if re.match(r'^http',p):
        #         yield Request(p,callback=self.getContentPage,meta=meta.copy())
        #     else:
        #         yield Request("{}{}".format(self.base_url,p),callback=self.getContentPage,meta=meta.copy())

    def getContentPage(self,response):
        meta = response.request.meta.copy()
        self.log('..................getContentPage')
        contentList = response.xpath('//ul[@class="dl_group"]//a')
        for content in contentList:
            href = content.xpath('@href').extract_first()
            title = content.xpath('text()').extract_first()
            print href,title
            meta['title'] = title
            if re.match(r'^http',href):
                self.log('href: %s' % href)
                return Request(href,callback=self.getDetailPage,meta=meta.copy())
            else:
                self.log('href: %s' % "{}{}".format(self.base_url,href))
                return Request("{}{}".format(self.base_url,href),callback=self.getDetailPage,meta=meta.copy())

    def getDetailPage(self,response):
        meta = response.request.meta.copy()
        self.log('..................getDetailPage')
        href = response.xpath('//div[@class="download_box]"//a[@class="download_btn"]/@href').extract_first()
        self.log(href)
        self.log('..................')
        return Request(href,callback=self.getDownloadLinkPage,meta=meta.copy())

    def getDownloadLinkPage(self,response):
        meta = response.request.meta
        self.log('.....................getDownloadLinkPage')
        self.log(response.xpath('//div[@class="move"]//a/@href').re(r'^http://xia3.*').extract_first())