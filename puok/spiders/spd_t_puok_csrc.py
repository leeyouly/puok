# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_csrcItem
import re
import random
import lxml
import time, datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

today = datetime.datetime.now()
day_datadate = today.strftime('%Y-%m-%d')
year_datadate = today.strftime('%Y')
last_year = int(year_datadate) - 1
last_update_date = datetime.datetime.now() - datetime.timedelta(days=10)

index = 1

#扑克财经需求--证监会新闻抓取
class PuokCSRC(scrapy.Spider):
    name = "spd_t_puok_csrc"
    start_urls = (
        'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'证监会')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_csrc'])

        # url = 'http://www.nea.gov.cn/20140521_1449.pdf'
        # request = scrapy.http.FormRequest(url, callback=self.parse_title)
        # yield request

        for page in range(0,3,1):
            if page == 0:
                titleurl = 'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/index.html'
            else :
                titleurl = 'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/index_' + str(page) + '.html'
            request = scrapy.http.Request(titleurl, callback=self.parse_title)
            yield request

    #解析文章标题以及url
    def parse_title(self, response):
        newsUl = response.xpath('//*[@id="myul"]')

        for newsList in newsUl:
            news = newsList.xpath('./li')
            for newsDetail in news:
                if newsDetail.xpath('./a/text()').extract() <>[]:
                    datadate = newsDetail.xpath('./span/text()').extract()[0]
                    newsTitle = newsDetail.xpath('./a/text()').extract()[0]
                    newsContentURL =  response.urljoin(newsDetail.xpath('./a/@href').extract()[0])
                    # print 'newsHref----> ' + newsHref
                    # print 'response.urljoin----> ' + response.urljoin(newsHref)
                    # print newsTitle
                    # newsContentURL = 'http://www.ndrc.gov.cn/xwzx/xwfb/'+newsHref.replace('./','')
                    request = scrapy.http.Request(newsContentURL, callback=self.parse_newsContent)
                    request.meta['datadate'] = datadate
                    request.meta['newsTitle'] = newsTitle
                    request.meta['newsContentURL'] = newsContentURL
                    # request.meta['news_type'] = response.meta['news_type']
                    yield request
                else:
                    print u'未找到url,暂停3到5秒重新请求--->' + response.url
                    time.sleep(random.uniform(3, 5))
                    request = scrapy.http.Request(response.url, callback=self.parse_title)
                    yield request

    #解析文章内容
    def parse_newsContent(self, response):
        datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y-%m-%d')
        imageurl = ''
        newsTitle = response.meta['newsTitle']
        newsContentURL = response.meta['newsContentURL']

        contentStr = response.body
        # 有一些公告就是pdf格式的，无法解析成html，用newstitle+newurl的方式存储在news_html中
        if 'PDF' in contentStr:
            global index
            print u'pdf第 ' + str(index) + u' 次打印'
            index = index + 1
            item = Puok_csrcItem()
            item['datadate'] = datadate
            item['news_title'] = newsTitle
            item['news_content'] = u''
            item['news_html'] = newsTitle + ' ' + response.url
            item['news_contenturl'] = newsContentURL
            item['news_imageurl'] = imageurl
            item['update_dt'] = datetime.datetime.now()
            yield item
        else:
            news_html= response.xpath('//div[@class="in_main"]/div[@class="content"]/div[3]').extract()
            if news_html <> []:
                news_html = news_html[0]
                html_parser = lxml.html.HTMLParser(encoding='gb2312', remove_comments=True)
                content_html_etree = lxml.html.fromstring(news_html, parser=html_parser)
                lxml.etree.strip_elements(content_html_etree, 'iframe', 'script', 'style')
                news_html = lxml.html.tostring(content_html_etree, encoding='utf-8').decode('utf-8')

                item = Puok_csrcItem()
                item['datadate'] = datadate
                item['news_title'] = newsTitle
                item['news_content'] = u''
                item['news_html'] = news_html
                item['news_contenturl'] = newsContentURL
                item['news_imageurl'] = imageurl
                item['update_dt'] = datetime.datetime.now()
                yield item
            else:
                print u'可能是请求过快，未解析到内容，暂停3到5秒重新请求-->' + response.url
                time.sleep(random.uniform(3, 5))
                request = scrapy.http.Request(newsContentURL, callback=self.parse_newsContent)
                request.meta['datadate'] = datadate
                request.meta['newsTitle'] = newsTitle
                request.meta['newsContentURL'] = newsContentURL
                yield request


