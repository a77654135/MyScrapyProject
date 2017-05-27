import scrapy

class QiushibaikeItem(scrapy.Item):
    author_img = scrapy.Field()
    author_name = scrapy.Field()
    content_href = scrapy.Field()
    content_str = scrapy.Field()
    thumb = scrapy.Field()
    vote = scrapy.Field()
    comments = scrapy.Field()