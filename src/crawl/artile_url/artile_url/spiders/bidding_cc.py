# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem
import re
'''
username: zhijuexinxi 
password: hrs19980127

we need get two cookies below by browser 
'__jsluid': "e611b830ab6ee68679137bb7d62ded01"
'__jsl_clearance' expired in an hour

we only can get 200 pages results
'''


class bidding(scrapy.Spider):
    name = 'bidding_1'
    allow_domains = ['chinabidding.cc']
    template_url = "http://www.chinabidding.cc/search/index.html?keyword=%s&date=365&search_field=%s"
    kw = ''
    curr_page = 1
    allitem = -1 #sum number of search result
    cookie = {
        '__jsluid': "e611b830ab6ee68679137bb7d62ded01",
        '__jsl_clearance': "1554775792.468|0|vNd03DFC0aOWRPvnnw%2B3XUjITBs%3D",
        'clientlogin': '463fFuRpQmdza_GRxhjSSsipCXXR0zA0bLDtcu2TJmzTVnJsgghQMjxnrrgb7ocYQcXtEps',
        'client_login_info': 'qQchn2MFO8yEYIAlIiwEJZefNY_cCw84d.1oWw'
    }

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    def start_requests(self):

        self.kw = getattr(self, 'kw', None)
        if self.kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return
        urls = [
                # self.template_url % (self.kw, '0'),
                self.template_url % (self.kw, '1')
                ]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookie, headers=self.header)

    def parse(self, response):
        #get article urls
        resulturls = response.xpath("//ul[@class='ul_list']//a/@href")
        for u in resulturls:
            item = CbItem()
            item['url'] = u.extract()
            print(item)
            yield item

         #get sum num of results
        if self.allitem < 0:
            contain_sum_itemnum = response.xpath("(//b[@style='color:red;'])[1]/text()").extract()
            if contain_sum_itemnum == []:
                return
            nums = re.findall('\d+',contain_sum_itemnum[0])
            if len(nums) == 0:
                return
            self.allitem = int(nums[0])
            print(self.allitem)
        #this web only get 200 pages information
        if self.curr_page * 20 < self.allitem and self.curr_page <= 200:
            self.curr_page += 1
            # u1 = self.template_url % (self.kw, '0') + '&page=' + str(self.curr_page)
            u2 = self.template_url % (self.kw, '1') + '&page=' + str(self.curr_page)
            yield scrapy.Request(url=u2, callback=self.parse, cookies=self.cookie, headers=self.header)
        else:
            return

