# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem

'''
username: zhijuexinxi
password: 123456

what we get is part of url , and we 
need to add pre_url like https://www.chinabidding.cn
to get complete url
'''


class BIDDING_CN(scrapy.Spider):
    name = 'spider_biddingcn'
    allow_domains = ['chinabidding.cn']
    template_url = "https://www.chinabidding.cn/search/searchzbw/search2?keywords=%s&rp=22&table_type=0&b_date=year"
    pre_url = 'https://www.chinabidding.cn'
    kw = ''
    c = {
        'accessId': 'be759b80-2db1-11e8-9292-47bcc2cedaa9',
        'CBL_SESSION':'8241f063d57df5bca6e095f6a1b917cee1bb3fa5-___'
                      'TS=1590775925690&___ID=1c5fb101-489f-446f-b376-4c0d8fd0dfbe',
        'SERVERID': '415587c0a4474a99267e61243891a333 | 1554778144 | 1554774405'
    }

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }

    def start_requests(self):
        self.kw = getattr(self, 'kw', None)
        if self.kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return
        urls = [
                self.template_url % self.kw
                ]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.c, headers=self.header)


    def parse(self, response):
        #get article urls
        resulturls = [response.xpath("//tbody//tr[@class='listrow1']/td[2]/a/@href"),
                      response.xpath("//tbody//tr[@class='listrow2']/td[2]/a/@href")]
        for resulturl in resulturls:
            for u in resulturl:
                item = CbItem()
                item['url'] = self.pre_url + u.extract()
                print(item)
                yield item

        #get next page
        next_page = response.xpath(u"//a[text() = '后一页']/@href").extract()
        if next_page == []:
            return
        next_url = self.pre_url + next_page[0]
        print(next_url)
        yield scrapy.Request(url=next_url, callback=self.parse, cookies=self.c, headers=self.header)


