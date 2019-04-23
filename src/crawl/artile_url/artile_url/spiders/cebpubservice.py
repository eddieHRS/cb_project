# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem
import re
import sys
import io

class mingyan(scrapy.Spider):
    name = "cebpubservice"
    allow_domains = ['cebpubservice.com']
    currentpage = 1
    kw = ''
    url = 'http://bulletin.cebpubservice.com/xxfbcmses/search/bulletin.html?' \
          'categoryId=88&industryName=G20&word=%s&page='

    def start_requests(self):
        self.kw = getattr(self, 'kw', None)
        if self.kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return
        self.url = self.url % self.kw
        url = self.url + str(self.currentpage)
        print(url)
        yield scrapy.Request(url=url, callback=self.parse, method='GET')

    def parse(self, response):
        #get article urls
        urls = response.xpath("//table[@class='table_text']//a/@href")
        for u in urls:
            item = CbItem()
            item['url'] = re.findall("'.*'", u.extract())[0].replace("'", '')
            print(item)
            yield item

        #get next page url
        n = response.xpath(u"//a[text() = '下一页']").extract()
        if len(n) == 0:
            print("len n = 0")
            return
        self.currentpage += 1
        url = self.url + str(self.currentpage)
        print(url)
        yield scrapy.Request(url=url, callback=self.parse)


