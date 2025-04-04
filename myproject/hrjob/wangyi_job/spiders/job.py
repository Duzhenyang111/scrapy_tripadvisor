import scrapy
import json
import re
import random
import time
from wangyi_job.items import BarDetailItem

class JobSpider(scrapy.Spider):
    name = "job"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["https://www.tripadvisor.com/Restaurants-g308272-zft10640-Shanghai.html"]
    def __init__(self):
        self.index = 0
    def parse(self, response):
        node_list = response.xpath('//*[@id="lithium-root"]/main/div[1]/div[4]/div/div/div/div[2]/div[5]/span')
        for node in node_list:
            item = BarDetailItem()
            item['url'] = response.urljoin(node.xpath('./div/div/div[1]/div/span/a/@href').extract_first())
            yield scrapy.Request(
                url = item['url'],
                callback = self.parse_detail,
                meta={'item':item})
        # 实现翻页（由于每一页的下一页位置不同，通过self.index去实现不同的翻页）
        if self.index == 0:
            part_url = response.xpath('//*[@id="lithium-root"]/main/div[1]/div[4]/div/div/div/div[2]/div[6]/div/div[1]/div/div/a/@href').extract_first()
        else:
            part_url = response.xpath('//*[@id="lithium-root"]/main/div[1]/div[4]/div/div/div/div[2]/div[6]/div/div[1]/div[2]/div/a/@href').extract_first()
        if part_url != None:
            self.index = 2
            next_url = response.urljoin(part_url)
            time.sleep(random.uniform(1, 10))
            yield scrapy.Request(next_url,callback=self.parse)
            
    def parse_detail(self,response):
        time.sleep(random.uniform(1, 3))
        item = response.meta['item']
        map_url = response.xpath('//*[@class="tXWuf"][1]/div[2]/a/@href').extract_first()
        match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', map_url)
        if match:
            item['lat'] = match.group(1)
            item['lon'] = match.group(2)
        item['name'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[2]/div[3]/div/div[1]/span/h1/text()').extract_first()
        item['city'] = "Shanghai"
        item['address'] = response.xpath('//*[@class="tXWuf"][1]/div[2]/a/div/div/div/text()').extract_first()
        item['cuisine'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[2]/div[3]/div/div[2]/span[3]/span[3]/a/span/text()').extract_first()
        match_phone = response.xpath('//*[@id="lithium-root"]/main/div/div/div[3]/div[1]/div[1]/div[1]/div[3]/a[2]/@href').extract_first()
        try:
            item['phone'] = match_phone.split('tel:')[1]
        except:
            item['phone'] = match_phone
        # match = re.search(r"\+\d{1,3} \d{1,4} \d{4} \d{4}", match_phone)
        # if match:
        #     item['phone'] = match.group()
        # else:
        #     item['phone'] = match_phone
        # item['phone'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[3]/div[1]/div[1]/div[1]/div[3]/a[2]/@href').extract_first().split('tel:')[1]
        item['rating'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[2]/div[3]/div/div[2]/span[1]/span/div/div/span/div/text()').extract_first()
        item['reviews_nr'] = str(json.loads(response.xpath('//*[@id="lithium-root"]/main/div/div/script/text()').get())["aggregateRating"]["reviewCount"])
        # item['url'] = response.url
        item['source'] = 'tripadvisor'
        # setting。py中设置打开中间件SeleniumMiddleware则可爬取website，否则爬取不到
        item['website'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[3]/div[1]/div[1]/div[1]/div[3]/a[1]/@href').extract_first()
        yield item