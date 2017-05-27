# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request


class QiushibaikeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/']

    base_url = r'http://www.qiushibaike.com'

    def parse(self, response):

        a_list1 = response.xpath("//div[@id='menu']/a[starts-with(@href,'/')]")
        for a in a_list1:
            href = a.xpath('@href').extract_first()
            menu = a.xpath("text()").extract_first()
            print u'href:{}   text:{}'.format(href,menu)


    # 解析页数
    def getPageList(self,response):
        pass