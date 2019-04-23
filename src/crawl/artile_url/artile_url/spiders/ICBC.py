# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem
import re
import time


class icbc(scrapy.Spider):
    name = 'icbc'
    allow_domains = ['icbc-ltd.com']
    template_url = "http://search.icbc-ltd.com/searchcenter/search.aspx?KeyWord=%s&rpage=%s&rkeyWord=%s&startIndex=%s"
    advance_text_url = 'http://search.icbc-ltd.com/searchcenter/advanceresult.aspx?KeyWord=%s&iftitle=0&pageCount=50&startIndex=%s'#50 results each page 全文搜索
    curr_page = 0
    kw = ''

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        self.kw = getattr(self, 'kw', None)
        print(self.kw)
        if self.kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return

        url = self.template_url % (self.kw, self.curr_page, self.kw, 15 * self.curr_page + 1)
        # url = self.advance_text_url % (self.kw , 50 * self.curr_page + 1)
        print(url)
        yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response):
        # time.sleep(5)
        urls = response.xpath("//a[@class='title']/@href")
        for u in urls:
            item = CbItem()
            item['url'] = u'%s' % u.extract()
            print(item['url'])
            yield item


        n = response.xpath("//span[@class='n']/../@href")
        if len(n) == 0 or self.curr_page >= 200:
            print("len n = 0")
            return
        self.curr_page += 1
        nextpage = self.template_url % (self.kw, self.curr_page, self.kw, 15 * self.curr_page + 1)
        # nextpage = self.advance_text_url % (self.kw , 50 * self.curr_page + 1)
        print(nextpage)
        yield scrapy.Request(url=nextpage, callback=self.parse)


