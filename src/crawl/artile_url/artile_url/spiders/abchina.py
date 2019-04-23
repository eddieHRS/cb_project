# -*- coding:utf-8 -*-
import scrapy
from artile_url.items import CbItem
import time
'''
sometimes http://query.abchina.com/search/cn.jsp is unreachable
dont know why

返回的数据
http://query.abchina.com/search/action/searchht.jsp



采用splash 来对JS渲染做处理

'''

class ABCHINA(scrapy.Spider):
    name = 'abchina'
    allow_domains = ['abchina.com']
    url = 'http://query.abchina.com/search/action/searchht.jsp'
    fd = {
        'keyword': '',
        'where': u'(DOCCONTENT=(方法) or DOCTITLE=(方法))',
        'basenames': '123123',
        'searchfield': 'ALLFIELD',
        'curpage': '4',
        'pagecount': '20',
        'classvalue1': 'ALL',
        'classfield1': 'CLASS1',
        'classvalue2': 'ALL',
        'classfield2': 'ALL',
        'classvalue3': 'ALL',
        'classfield3': 'CLASS3',
        'istong': '0',#同音
        'isclass': '1',
        'znkz': '1',
        'searchtype': 'normal',
        'sortfield': '-HOTVALUE,-DOCRELTIME',
        'fantiorjianti': '0',
        'searchList': 'DOCTITLE,DOCPUBURL',
        'searchListName': u'标题,发布地址'
        # 'searchList': 'DOCTITLE,DOCPUBURL,DOCCONTENT,RELEVANCE,DOCRELTIME,CLASS1',
        # 'searchListName': u'标题,发布地址,正文,相关度,撰写时间,所属栏目'

    }

    def start_requests(self):
        kw = getattr(self, 'kw', None)
        if kw is None:
            print("please enter key word, like -a kw=yourkeyword")
            return
        self.fd['keyword'] = kw
        self.fd['where'] = '(DOCCONTENT=(%s) or DOCTITLE = (%s))' % (kw, kw)
        print(self.fd['where'])
        print(self.fd['keyword'])

        yield scrapy.FormRequest(url=self.url, formdata=self.fd, callback=self.parse, method='POST')

    def parse(self, response):
        print("i am in parse")

        content = response.xpath("//DOCPUBURL/text()")
        for c in content:
            item = CbItem()
            item['url'] = c.extract()
            print(item)
            yield item

        #get next page
        next_page = response.xpath("//PAGES/text()").extract()
        print(next_page[0], self.fd['curpage'])
        if next_page[0] <= self.fd['curpage']:
            print("dfd")
            return
        self.fd['curpage'] = str(int(self.fd['curpage']) + 1)

        yield scrapy.FormRequest(url=self.url, formdata=self.fd, callback=self.parse, method='POST')
