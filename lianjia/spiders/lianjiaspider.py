import math
import urllib.parse
import scrapy
from scrapy_redis.spiders import RedisSpider

from lianjia.items import LianjiaItem

count = 1


class LianjiaspiderSpider(RedisSpider):
    name = 'lianjiaspider'
    allowed_domains = ['lianjia.com']
    # start_urls = ['https://tj.fang.lianjia.com/loupan/']
    redis_key = 'lianjiaspider'

    def parse(self, response):
        # print(response.url.split('/')[2] + '/' + response.url.split('/')[3])
        li_list = response.xpath('//ul[@class="resblock-list-wrapper"]/li')
        for temp in li_list:
            item = LianjiaItem()
            item['resblock_price_url'] = temp.xpath('.//img/@src').extract_first()
            item['resblock_name'] = temp.xpath('.//div[@class="resblock-name"]/a/text()').extract_first()
            item['resblock_type'] = temp.xpath('.//div[@class="resblock-name"]/span[@class="resblock-type"]/text()').extract_first()
            item['resblock_status'] = temp.xpath('.//div[@class="resblock-name"]/span[@class="sale-status"]/text()').extract_first()
            location1 = temp.xpath('.//div[@class="resblock-location"]/span[1]/text()').extract_first()
            location2 = temp.xpath('.//div[@class="resblock-location"]/span[2]/text()').extract_first()
            around = temp.xpath('.//div[@class="resblock-location"]/a/text()').extract_first()
            item['resblock_location'] = location1 if location1 else "" + '-' + location2 if location2 else "" + '-' + around if around else ""
            item['resblock_room'] = temp.xpath('.//a[@class="resblock-room"]/span/text()').extract()
            item['resblock_area'] = temp.xpath('.//div[@class="resblock-area"]/span/text()').extract_first()
            item['resblock_tag'] = temp.xpath('.//div[@class="resblock-tag"]/span/text()').extract()
            item['resblock_price'] = temp.xpath('.//div[@class="main-price"]/span[@class="number"]/text()').extract_first() + r'元/㎡(均价)'
            item['resblock_second'] = temp.xpath('.//div[@class="second"]/text()').extract_first()
            detail_url = temp.xpath('.//div[@class="resblock-name"]/a/@href').extract_first()
            item['detail_url'] = urllib.parse.urljoin(response.url, detail_url)
            print(item)

        # 一种处理js翻页的方法
        # 抓取的当前也永远是1
        current_url_num = response.xpath('//div[@class="page-box"]/@data-current').extract_first()
        # 获取所有数据条数
        all_data = response.xpath('//div[@class="page-box"]/@data-total-count').extract_first()
        current_page_num = int(current_url_num) if current_url_num else ''
        # 除以每页条数获得所有页数
        all_page_num = math.ceil(int(all_data) / 10) if all_data else ''
        # 可能有的页数已经没有数据，判断li_list是否匹配到，空页不抓取
        if current_page_num and all_page_num and li_list:
            global count
            if int(current_page_num) + count - 1 < int(all_page_num):
                yield scrapy.Request(
                    url='https://' + response.url.split('/')[2] + '/' + response.url.split('/')[3] + '/pg{}/'.format(int(current_page_num) + count),
                    callback=self.parse)
                print('url=', 'https://' + response.url.split('/')[2] + '/' + response.url.split('/')[3] + '/pg{}/'.format(int(current_page_num) + count))
                count += 1