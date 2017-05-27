from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random

class RotateUserAgentMiddleware(UserAgentMiddleware):
    """This middleware allows spiders to override the user_agent"""

    us_list = [
        r'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36 QIHU 360SE',
        r'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        r'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        r'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        r'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        r'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        r'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        r'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        r'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
        r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    ]


    def process_request(self, request, spider):
        request.headers.setdefault(b'User-Agent', random.choice(self.us_list))