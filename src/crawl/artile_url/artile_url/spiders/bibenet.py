# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem

'''
we can only get 100 pages results
'''


class bidding(scrapy.Spider):
    name = 'bibenet'
    allow_domains = ['bibenet.com']
    url = 'https://www.bibenet.com/search'
    fd = {
        'messageLikes': '',
        'pageNum': '1'
    }
    kw = ''
    totalpage = -1

    def start_requests(self):
        '''
        get keyword and create first request url
        :return:
        '''
        self.kw = getattr(self, 'kw', None)
        if self.kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return
        self.fd['messageLikes'] = self.kw
        yield scrapy.FormRequest(url=self.url, formdata=self.fd, callback=self.parse)

    def parse(self, response):
        '''
        parse url from response and get next page
        :param response:
        :return:
        '''
        #get urls
        urls = response.xpath("//tr//a/@href")
        for u in urls:
            item = CbItem()
            item['url'] = u.extract()
            print(item)
            yield item

        #get nextpage
        pagenum = int(response.xpath("//input[@name='pageNum']/@value").extract()[0])
        if self.totalpage == -1:
            self.totalpage = int(response.xpath("//input[@name='totalPage']/@value").extract()[0])
        # print(pagenum, self.totalpage)
        if pagenum < self.totalpage and pagenum <= 100:
            self.fd['pageNum'] = str(pagenum+1)
            # print(self.fd)
            yield scrapy.FormRequest(url=self.url, formdata=self.fd, callback=self.parse)
        else:
            return
