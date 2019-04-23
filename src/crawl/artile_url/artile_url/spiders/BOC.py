# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem
import re
import sys
import io


class BOC(scrapy.Spider):
    name = "boc"
    allow_domains = ['bankofchina.com']
    url = 'http://srh.bankofchina.com/search/sitesearch/index.jsp'
    fd = {
        'Stype': '1',
        'preSWord': '',
        'searchColumn': 'all',
        'sword': '',
        'order': '2',
        'button2': u'检索',
        'page': '1'
    }

    def start_requests(self):
        kw = getattr(self, 'kw', None)
        if kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return
        self.fd['sword'] = kw
        yield scrapy.FormRequest(url=self.url, formdata=self.fd, callback=self.parse)

    def parse(self, response):
        #get article urls
        urls = response.xpath("//a[@class='fsm']/@href")
        for u in urls:
            item = CbItem()
            item['url'] = u.extract()
            print(item)
            yield item
        #get next page
        n = response.xpath(u"//a[text() = '下一页']/@onclick").extract()
        if len(n) == 0:
            print("len n = 0")
            return
        ne = re.findall('\d+',n[0])
        print(ne)
        self.fd['page'] = ne
        yield scrapy.FormRequest(url=self.url, formdata=self.fd, callback=self.parse)


