# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem


class CFCPN(scrapy.Spider):
    name = "cfcpn"
    allow_domains = ['cfcpn.com.cn']
    kw = ''
    template_url = 'http://www.cfcpn.com/plist/caigou?kflag=0&keyword=%s&keywordType=0&pageNo='

    def start_requests(self):
        self.kw = getattr(self, 'kw', None)
        if self.kw is None:
            print("kw can not be empty")
            return
        url = self.template_url % self.kw
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = CbItem()
        content = response.xpath("//p[@class='cfcpn_list_title']/a/@href").extract()
        for part_url in content:
            item['url'] = "http://www.cfcpn.com" + part_url
            print(item)
            yield item
        nextpage = response.xpath(u"//a[text()='>']/@href").extract()
        # print(nextpage)
        if len(nextpage) == 0:
            return
        else:
            print(nextpage[0])
            yield scrapy.Request(url=nextpage[0], callback=self.parse)