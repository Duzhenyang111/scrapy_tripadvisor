import scrapy
import json
import re
from wangyi_job.items import BarDetailItem

class DoubanSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["https://www.tripadvisor.com/Restaurant_Review-g308272-d7227449-Reviews-Aura_Lounge_Jazz_Bar_The_Ritz_Carlton_Shanghai_Pudong-Shanghai.html"]
    #https://www.tripadvisor.com/Restaurant_Review-g308272-d5260581-Reviews-Sky_Dome_Bar-Shanghai.html
    #https://www.tripadvisor.com/Restaurant_Review-g308272-d2257238-Reviews-Flair_Rooftop-Shanghai.html
    def parse(self, response):
        item = BarDetailItem()
        map_url = response.xpath('//*[@class="tXWuf"][1]/div[2]/a/@href').extract_first()
        match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', map_url)
        if match:
            item['lat'] = match.group(1)
            item['lon'] = match.group(2)
        item['name'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[2]/div[3]/div/div[1]/span/h1/text()').extract_first()
        item['city'] = "Shanghai"
        item['address'] = response.xpath('//*[@class="tXWuf"][1]/div[2]/a/div/div/div/text()').extract_first()
        item['cuisine'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[2]/div[3]/div/div[2]/span[3]/span[3]/a/span/text()').extract_first()
        item['phone'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[3]/div[1]/div[1]/div[1]/div[3]/a[2]/@href').extract_first().split(':')[1]
        # item['rating'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[2]/div[3]/div/div[2]/span[1]/span/div/div/span/div/text()').extract_first()
        item['rating'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[2]/div[3]/div/div[2]/span[1]/span/div/div/div/div/a/div/text()[2]').extract_first()
        
        item['reviews_nr'] = str(json.loads(response.xpath('//*[@id="lithium-root"]/main/div/div/script/text()').get())["aggregateRating"]["reviewCount"])
        item['url'] = response.url
        item['source'] = 'tripadvisor'
        item['website'] = response.xpath('//*[@id="lithium-root"]/main/div/div/div[3]/div[1]/div[1]/div[1]/div[3]/a[1]/@href').extract_first()
        print(item)
        # print(response.xpath('//*[@id="lithium-root"]/main/div/div/div[3]/div[1]/div[1]/div[3]').extract())
        
        
        yield item
        # print(node_list)
        pass
        
        # part_url = response.xpath(f'//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract_first()
        # # print(response.urljoin(part_url))
        # if part_url != None:
        #     # self.index += 2
        #     next_url = response.urljoin(part_url)
        #     yield scrapy.Request(
        #         url = next_url,
        #         callback = self.parse)