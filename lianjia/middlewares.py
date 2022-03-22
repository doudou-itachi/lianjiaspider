# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

import requests
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from lianjia.settings import USER_AGENT_LIST, IP_PROXY_URL


class RandomProxy(object):

    def __init__(self):
        self.current_proxy = None

    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = user_agent
        if 'proxy' not in request.meta:
            # 请求代理
            self.update_proxy()
            request.meta['proxy'] = self.current_proxy.proxy if self.current_proxy else ''

    def process_response(self, request, response, spider):
        # 如果对方重定向（302）去验证码的网页，换掉代理IP
        # 'captcha' in response.url 指的是有时候验证码的网页返回的状态码是200，所以用这个作为辨识的标志
        if response.status != 200 or 'captcha' in response.url:
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
            self.update_proxy()
            print('%s代理失效' % self.current_proxy.proxy)
            request.meta['proxy'] = self.current_proxy.proxy
            return request
        return response

    def update_proxy(self):
        if not self.current_proxy or self.current_proxy.blacked:
            # 豌豆生成的api,但是太慢了
            url = IP_PROXY_URL
            response = requests.get(url=url)
            data_dict = random.choice(response.text.split()).split(':')
            # print(data_dict)
            data = {"ip": data_dict[0], 'port': data_dict[1]}
            # print(data)
            proxy_model = ProxyModel(data)
            print('重新获取了一个代理：%s' % proxy_model.proxy)
            self.current_proxy = proxy_model
            print(self.current_proxy)
            # return proxy_model
        # self.lock.release()


class ProxyModel(object):
    def __init__(self, data):
        self.ip = data['ip']
        self.port = data['port']
        self.proxy = 'http://' + '%s:%s' % (self.ip, self.port)
        # 代理是否已经被拉入黑名单了
        self.blacked = False


class LianjiaSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LianjiaDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
