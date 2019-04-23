# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem

pre = "http://iframe.chinapost.com.cn/jsp/util/Search.jsp?community=ChinaPostJT&lucenelist=1813902036&q=%s&"
domain = "http://www.chinapost.com.cn"

class chinapost(scrapy.Spider):
    name = "chinapost"
    allow_domains = ['chinapost.com.cn']

    def start_requests(self):
        kw = getattr(self,'kw',None)
        if kw == None:
            print("kw can not be empty")
            return
        else:
            urls = [pre % kw]
            for url in urls:
                print(url)
                yield  scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):


        # "http://iframe.chinapost.com.cn/jsp/util/Search.jsp?community=ChinaPostJT&lucenelist=1813902036&q=%E6%95%B0%E6%8D%AE&"
        # "http://iframe.chinapost.com.cn/jsp/util/Search.jsp?node=0&community=ChinaPostJT&lucenelist=1813902036&lang=1&type=0&q=%E6%95%B0%E6%8D%AE&pos=10"
        # "http://iframe.chinapost.com.cn/jsp/util/Search.jsp?node=0&community=ChinaPostJT&lucenelist=1813902036&lang=1&type=0&q=%E6%95%B0%E6%8D%AE&pos=20"
        item = CbItem()
        content = response.xpath("//td[@id='searchsubject']/a/@href").extract()
        for part_url in content:
            item['url'] = domain + part_url
            # print(item)
            yield item
        nextpage = response.xpath(u"//a[text()='下一页']/@href").extract()
        # print(nextpage)
        if len(nextpage) == 0:
            return
        else:
            print(nextpage[0])
            yield scrapy.Request(url=nextpage[0],callback=self.parse)