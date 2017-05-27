# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http.request import Request
from MyScrapyProject.items.qiushibaike_items import QiushibaikeItem


class QiushibaikeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/']

    base_url = r'http://www.qiushibaike.com'

    def parse(self, response):
        a_list = response.xpath("//div[@id='menu']/a[starts-with(@href,'/')]")
        for a in a_list:
            href = a.xpath('@href').extract_first()
            menu = a.xpath("text()").extract_first()
            meta = {"menu": menu}
            yield Request('{}{}'.format(self.base_url,href),callback=self.getPageList,meta=meta)

    # 解析页数
    def getPageList(self,response):
        href = response.xpath("//ul[@class='pagination']/li[last()-1]/a/@href").extract_first()
        if href:
            count = re.findall(r'.*/(\d+)\?.*',href)
            if count and len(count):
                count = int(count[0])
                for i in range(1,count+1):
                    link = re.sub(r'/\d+\?','/{}?'.format(i),href,1)
                    yield Request('{}{}'.format(self.base_url,link),callback=self.getContentList,meta=response.meta)


    #解析当页内容列表
    def getContentList(self,response):
        content_list = response.xpath(r'//div[@id="content-left"]/div')
        for content in content_list:
            author_img = content.xpath(r'div[@class="author clearfix"]//img[starts-with(@src,"//pic")]/@src').extract_first()
            author_name = content.xpath(r'div[@class="author clearfix"]//h2/text()').extract_first()
            content_href = content.xpath(r'a[@class="contentHerf"]/@href').extract_first()
            content_str = content.xpath(r'a[@class="contentHerf"]/div/span/text()').extract()
            thumb = content.xpath(r'div[@class="thumb"]/a/img[starts-with(@src,"//pic")]/@src').extract_first()
            vote = content.xpath(r'div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract_first()
            comments = content.xpath(r'div[@class="stats"]/span[@class="stats-comments"]//i/text()').extract_first()

            item = QiushibaikeItem()
            item["author_img"] = "http:{}".format(author_img)
            item["author_name"] = author_name
            item["content_href"] = "{}{}".format(self.base_url,content_href)
            item["content_str"] = content_str
            item["thumb"] = "http:{}".format(thumb)
            item["vote"] = vote
            item["comments"] = comments
            yield item
