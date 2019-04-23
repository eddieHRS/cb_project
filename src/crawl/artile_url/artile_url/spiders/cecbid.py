# -*- coding:utf-8 -*-

import scrapy
from artile_url.items import CbItem
import re

'''
username :eddie12138
password :123456

only can crawl 100 pages
'''
class cecbid_spider(scrapy.Spider):
    name = 'cecbid'
    allow_domains = ['cecbid.org.cn']
    url = 'http://so.cecbid.org.cn/so.php?t=tender&d=&a=&q='
    curr_page = 1
    kw = ''

    def start_requests(self):
        self.kw = getattr(self, 'kw', None)
        if self.kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return
        self.url += self.kw
        print(self.url)
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        #get article urls
        contents = response.xpath("//a[@class = 'text-success']/@href")
        for c in contents:
            item = CbItem()
            item['url'] = c.extract()
            print(item)
            yield item

        #get next page url
        contain_sum_itemnum = response.xpath("((//small[@class = 'text-muted'])[last()-1]/text())[last()]").extract()
        nums = re.findall(u'\d+ 个', contain_sum_itemnum[0])
        if len(nums) == 0:
            return
        num = re.findall(('\d+'), nums[0])
        print(num)
        n = int(num[0]) if len(num) > 0 else 0
        if self.curr_page * 10 < n:
            self.curr_page += 1
            u = self.url + '&p=' + str(self.curr_page)
            print(u)
            yield scrapy.Request(url=u, callback=self.parse)
        else:
            return


