# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Xuexi111Item(scrapy.Item):
    bookName = scrapy.Field()
    downloadLink = scrapy.Field()
    thunderDownloadLink = scrapy.Field()
    originalUrl = scrapy.Field()
    mainCategory = scrapy.Field()
    detailCategory = scrapy.Field()

class XicidailiItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    address = scrapy.Field()
    isAnonymous = scrapy.Field()
    type = scrapy.Field()
    speed = scrapy.Field()
    connectTime = scrapy.Field()
    survivalTime = scrapy.Field()
    verifyTime = scrapy.Field()

class ChinacaipuItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    imgSrc = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()


class QiushibaikeItem(scrapy.Item):
    category = scrapy.Field()
    author_img = scrapy.Field()
    author_name = scrapy.Field()
    content_href = scrapy.Field()
    content_str = scrapy.Field()
    thumb = scrapy.Field()
    vote = scrapy.Field()
    comments = scrapy.Field()
