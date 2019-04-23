执行命令示例：
python -m scrapy crawl ccgp_gov_cn  -a kw=节点  -o j.csv


带登录的模板bidcenter.py
jsp  formrequest的模板 BOC

关键词：区块链 节点 电子合同 数据 政务 签名 平台

数据全部存放在data文件夹下
爬虫放在spider目录下


Done
1）中国招标投标网 http://www.cecbid.org.cn/ （需注册为会员）  eddie12138  123456
只能爬取100页数据
数据路径：data/cecbid
爬虫路径：spiders/cecbid.py


Done
2）中国采购招标网 http://www.chinabidding.cc/  （需注册会员，等级权限） zhijuexinxi hrs19980127
需要登录，cookie
第一次访问返回一个加密的js文件，需要通过这个文件生成一个新的cookie，然后再去访问界面
解决方案：直接携带'__jsluid': "e611b830ab6ee68679137bb7d62ded01",
200页之后无法获得信息  仅提供前200页信息
        '__jsl_clearance' :
        cookie去访问，这两个cookie从浏览器获得
        cookie会过期，需要手动修改

Done
3）采购与招标网 https://www.chinabidding.cn/   （关键信息注册登陆查看）
zhijuexinxi     123456
url格式     https://www.chinabidding.cn/search/searchzbw/search2?keywords=区块链&page=2&rp=22&table_type=0&b_date=year
下一页的url  "//a[text() = '后一页']/@href"
文章url      "//
div[@id='txt']//@href"  得到的不完整 前面需要加上 https://www.chinabidding.cn


Done
4）中国政府采购网  http://www.ccgp.gov.cn/
数据指定范围为  2018/9/25  到 2019/3/26
数据路径：data/ccgp_gov_cn
爬虫路径：spiders/ccgp_gov_cn.py


Done
5）千里马招标网 http://www.qianlima.com/zbdw/  （免费注册，查看免费招标项目信息）
13817136871
注意：此处传入参数时，不知道为何中文乱码，所以直接传入 中文的utf-8编码,网站采用的gbk

Done
6）比比网 https://www.bibenet.com/search/（免费注册，查看免费招标项目信息）
最多100页


Done
7）采招网 https://www.bidcenter.com.cn/zhaobiao/（注册方可查看免费招标项目信息）
需要登陆过程
在搜索关键词数据的时候遇到了反爬措施
需要验证 ip被封


8）中国金融集中采购网 http://www.cfcpn.com/

Done
9）中国电力招标网  https://zgjsyh.dlzb.com/  （部分可免费查看，重要信息需会员查看）
需登录
https://denglu.dlzb.com/
https://www.dlzb.com/zb/search.php?kw=%E5%8C%BA%E5%9D%97%E9%93%BE&fields=3&page=1
usrname：zhijue   password：123456

非会员只能50页

节点 完成
区块链 完成
政务 50
数据 50
签名 完成
平台 50

Done
10）中国银行-关于中行-采购公告  http://www.boc.cn/aboutboc/bi6/

Done
11）中国邮政-采购公告公示-邮政储蓄银行 http://www.chinapost.com.cn/html1/category/181313/7338-1.htm

Done
12）中国招标投标公共服务平台  www.cebpubservice.com
如果采用提交表单类型，返回的html含有嵌套iframe，比较难处理，直接采用request的类型
http://bulletin.cebpubservice.com/?industryName=G20&word=%s&categoryID=88&page=1

抓取信息行业的 industy=G20相关信息




13）中国工商银行-公司业务-业务动态  http://www.icbc.com.cn/ICBC/公司业务/业务动态/
有两种搜索 普通搜索和高级搜索  普通搜索和高级的全文搜索并无区别
全文搜索的内容包含标题搜索   全文搜索还是标题搜索，看istitle的值   还可以指定时间


14）中国农业银行-关于农行-采购公告  http://www.abchina.com/cn/AboutABC/cggg/
返回的网页的 数据的div一直是 正在载入，请稍后的状态
需要js动态渲染
