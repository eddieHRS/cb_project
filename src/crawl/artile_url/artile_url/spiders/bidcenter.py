# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem

'''
anti-crawl happened and one ip will be banned in several hours

'''


class bidding(scrapy.Spider):
    name = 'bidcenter'
    allow_domains = ['bidcenter.com.cn']
    template_url = "https://search.bidcenter.com.cn/search?keywords=%s&page="
    login_url = "https://sso.bidcenter.com.cn/member_login"
    current_page = 0
    kw = ''
    pre_url = 'https://www.bidcenter.com.cn'
    login_info = {
        'name' : '13817136871',
        'pwd'  : '123456'
    }

    c = {
        'accessId': 'be759b80-2db1-11e8-9292-47bcc2cedaa9',
        'CBL_SESSION':'8241f063d57df5bca6e095f6a1b917cee1bb3fa5-___TS=1590775925690&___ID=1c5fb101-489f-446f-b376-4c0d8fd0dfbe',
        'SERVERID': '415587c0a4474a99267e61243891a333 | 1554778144 | 1554774405'
    }
    header = {
        'User-Agent': "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    }



    def start_requests(self):
        '''
        first request login page and then login
        callback self.afterlogin()
        :return:
        '''
        self.kw = getattr(self, 'kw', None)
        if self.kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return
        yield scrapy.FormRequest(url=self.login_url, headers=self.header, formdata=self.login_info, callback=self.afterlogin)




    def afterlogin(self,response):
        '''
        after login, start to request and get urls
        :param response:
        :return:
        '''
        urls = [
            self.template_url % (self.kw) + '1'
        ]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header)


    def parse(self, response):
        #get articles urls
        resulturl = response.xpath("//td[@class='zb_title']/a/@href")
        for u in resulturl:
            item = CbItem()
            item['url'] = u.extract()
            print(item)
            yield item

        #get nextpage url
        next_page = response.xpath(u"//a[text()='下一页']/@href").extract()
        if next_page == []:
            return
        self.current_page += 1
        next_url = self.template_url % self.kw + str(self.current_page)
        print(next_url)
        yield scrapy.Request(url=next_url, callback=self.parse, headers=self.header)


