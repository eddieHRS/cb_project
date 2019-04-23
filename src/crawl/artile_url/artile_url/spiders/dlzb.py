# -*- coding:utf-8 -*-
import scrapy
import time
from artile_url.items import CbItem
import re

'''
get nearly 20 pages and crawl will exit
this need some update

if you are not vip only 50 pages you can request

'''


class bidding(scrapy.Spider):
    name = 'dlzb'
    allow_domains = ['dlzb.com']
    template_url = "https://www.dlzb.com/zb/search.php?kw=%s&fields=3&page="
    login_url = "https://denglu.dlzb.com/"

    cookie = {
        '__jsluid': '1db29ff9f6780c7379ccb7e5aedd070c'
    }

    login_info = {
        'username' : 'zhijue',
        'pwd'  : '123456',
        # 'callback' : '1555032885646'
    }
    current_page = 51

    kw = ''

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }

    def start_requests(self):
        self.kw = getattr(self, 'kw', None)
        if self.kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return

        yield scrapy.FormRequest(url=self.login_url, headers=self.header, formdata=self.login_info, callback=self.afterlogin)

    def afterlogin(self,response):
        urls = [
            self.template_url % (self.kw) + str(self.current_page)
        ]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header, cookies=self.cookie)

    def parse(self, response):

        #获取数据
        time.sleep(2.0)
        resulturl = response.xpath("//a[@class='gccon_title']/@href")
        for u in resulturl:
            item = CbItem()
            item['url'] = u.extract()
            print(item)
            yield item

        #获取下一页
        next_page = response.xpath(u"//div[@class='pages']").extract()
        # print(next_page)
        if next_page == []:
            return
        self.current_page += 1
        next_url = self.template_url % self.kw + str(self.current_page)
        print(next_url)
        yield scrapy.Request(url=next_url, callback=self.parse, headers=self.header,cookies=self.cookie)
