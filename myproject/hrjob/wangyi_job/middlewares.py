# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html




import random
import time
from fake_useragent import UserAgent
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse
from scrapy import signals
import base64
from wangyi_job.settings import PROXIE_LIST

# 针对动态页面的请求
class SeleniumMiddleware(object):
    options = webdriver.FirefoxOptions()
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Connection': 'keep-alive',
    }

    def process_request(self, request, spider):
        # 设置无头选项
        url = request.url
        
        # if 'Restaurant_Review' in url:
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(10)
        body = driver.page_source
        driver.close()
        return HtmlResponse(url, body=body, encoding='utf-8', request=request)

# 随机UserAgent
class RandomUserAgent(object):
    def process_request(self, request, spider):
        print(request.headers['User-Agent'])
        ua = UserAgent().random
        request.headers['User-Agent'] = ua
        print(request.headers['User-Agent'])

# 随机代理,代理池写进settings。PROXIE_LIST
class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIE_LIST)
        # request.meta['proxy'] = proxy['ip_port']
        print(proxy)
        if 'user_password' in proxy:
            b64_up = base64.b64encode(proxy['user_passwd'].encode('utf-8'))
            request.headers['Proxy-Authorization'] = 'Basic ' + b64_up.decode('utf-8')
            request.meta['proxy'] = proxy['ip_port']
        else:
            request.meta['proxy'] = proxy['ip_port']








# from scrapy import signals

# # useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter


# class WangyiJobSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.

#         # Should return None or raise an exception.
#         return None

#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.

#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i

#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.

#         # Should return either None or an iterable of Request or item objects.
#         pass

#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.

#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r

#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)


# class WangyiJobDownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.

#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None

#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.

#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response

#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.

#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass

#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)
