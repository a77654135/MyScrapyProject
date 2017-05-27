# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.http import Request
from MyScrapyProject.items.items import ChinacaipuItem

class ChinacaipuSpider(scrapy.Spider):
    name = 'chinacaipu'
    allowed_domains = ['chinacaipu.com']
    start_urls = [
        'http://www.chinacaipu.com/menu/jiachangcaipu/index.html',
        'http://www.chinacaipu.com/menu/chinacaipu/index.html',
        'http://www.chinacaipu.com/menu/foreignshipu/index.html',
        'http://www.chinacaipu.com/menu/hongpei/index.html',
        'http://www.chinacaipu.com/menu/chufang/index.html',
    ]
    base_url = r'http://www.chinacaipu.com'

    # custom_settings = {
    #     "IMAGES_STORE": os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),'media/chinacaipu'),
    #     "IMAGES_EXPIRES": 30,
    #     "IMAGES_THUMBS": {
    #         'small':(50,50),
    #         'big':(270,270),
    #     },
    #     "IMAGES_MIN_HEIGHT": 0,
    #     "IMAGES_MIN_WIDTH": 0,
    #     'ITEM_PIPELINES': {
    #         'MyScrapyProject.pipelines.ChinacaipuPipelines.ChinacaipuImagePipeline': 400,
    #     }
    # }

    def parse(self, response):
        a_list = response.xpath('//ul[@class="c_conlist"]/li')
        category = response.xpath(r'//div[@class="cd_men_tit"]/h1/text()').extract_first()
        for li in a_list:
            item = ChinacaipuItem()
            item['category'] = category
            item['url'] = li.xpath('div/a/@href').extract_first()
            item['imgSrc'] = li.xpath('div//img/@src').extract_first()
            item['description'] = li.xpath('font/text()').extract_first()
            item['name'] = li.xpath('strong/a/text()').extract_first()
            yield item

        page = response.xpath('//div[@class="page"]/a/@href').extract()
        for p in page:
            yield Request("{}{}".format(self.base_url,p),callback=self.parse)


if __name__ == '__main__':
    print os.path.join(os.path.abspath(os.path.dirname(__file__)),'media/chinacaipu')


