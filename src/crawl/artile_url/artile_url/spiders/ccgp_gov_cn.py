# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem
import re


class mingyan(scrapy.Spider):
    name = "ccgp_gov_cn"
    allow_domains = ['ccgp.gov.cn']
    kw = ''
    template_url = "http://search.ccgp.gov.cn/bxsearch?searchtype=1&dbselect=bidx&timeType=5" \
                   "&start_time=2018\\09\\25&end_time=2019\\03\\26&kw=%s&page_index="

    def start_requests(self):
        self.kw = getattr(self, 'kw', None)
        if self.kw is None:
            print('please enter your key word')
            return
        urls = [
            self.template_url % self.kw + '1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):
        #get article urls
        context = response.xpath("//div[@class = 'vT-srch-result-list']//li/a/@href")
        for each in context:
            item = CbItem()
            item['url'] = each.extract()
            yield item

        #get next page url
        t = response.xpath("//p[@class='pager']/script[1]").extract()
        if len(t) > 0:
            text = t[0]
            curr = re.findall('\d+', re.findall('current: \d+', text)[0])[0]
            size = re.findall('\d+', re.findall('size: \d+', text)[0])[0]
            print(curr, size)
            if int(curr) + 1 < int(size):
                newurl = self.template_url + next
                print(newurl)
                yield scrapy.Request(url=newurl, callback=self.parse)
