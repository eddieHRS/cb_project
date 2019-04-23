# -*- coding: utf-8 -*-
import scrapy
from artile_url.items import CbItem

'''
we get keyword from terminal is utf8,but in url we need
gbk,so we need translate



'''


class QianlimaSpider(scrapy.Spider):
    name = 'qianlima'
    allowed_domains = ['qianlima.com']
    cookie = {
        '__jsluid': "a56107d6c32f2c1f67746813fc6da9e8",
        '__jsl_clearance': "1554799244.815|0|1x3erY7I6B2OUTB%2Bok%2FFoXjWYRE%3D",
        'fromWhereUrl' : 'http://search.qianlima.com/search.jsp?p_area=-1&p_type=0&p_state=-1&p_tflt=-1&p_xs=1&q_mod=2&q_kat=0&q_kw=',
        'qlm_username':'13817136871',
        'qlm_password':'uogEp8Kuj38EEUU7foBgRmfEujUoUCUu',
        'JSESSIONID':'79BD2B5F758B0C078F14AD2273D42BA8.tomcat1',
        'gr_user_id':'e7da3b56-44cb-41c2-9ac7-2ed55e9184dd'
    }
    formdata = {
        'q':'',
        'Submit':'+'
    }
    header = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }

    def start_requests(self):
        kw = getattr(self, 'kw', None)
        if kw is None:
            print("no keyword")
            return
        starturl='http://search.qianlima.com/search.jsp?q=' + kw.decode('utf8').encode('gbk')
        print(starturl)
        yield scrapy.Request(url=starturl, callback=self.parse, cookies=self.cookie,  headers=self.header)

    def parse(self, response):
        content = response.xpath("//td[@class='matter']/a/@href")
        for i in content:
            item = CbItem()
            item['url'] = i.extract()
            print(item)
            yield item

        nextpage = response.xpath(u"//a[text() = '下一页']/@href")
        if nextpage == []:
            return
        nexturl = nextpage.extract()[0]
        print(nexturl)
        yield scrapy.Request(url=nexturl, callback=self.parse, cookies=self.cookie, headers=self.header)

