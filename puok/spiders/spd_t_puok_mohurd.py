# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_mohurdItem
import re
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


#扑克财经需求--中国人民共和国住房和城乡建设部
class PuokMohurd(scrapy.Spider):
    name = "spd_t_puok_mohurd"
    start_urls = (
        'http://www.mohurd.gov.cn/xwfb/index.html',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'中华人民共和国住房和城乡建设部')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_mohurd'])

        start_url = 'http://www.mohurd.gov.cn/xwfb/index'
        for page in range(1,3,1):
            if page == 1:
                url = start_url + '.html'
            else:
                url = start_url + '_'+ str(page) + '.html'
            request = scrapy.http.FormRequest(url, callback=self.parse_title)
            # request.meta['pagetype'] = pagetypeDict[key]
            yield request

    #解析文章标题以及url
    def parse_title(self, response):
        aa= 'aaa'
        titleList = response.xpath('/html/body/table/tbody/tr[2]/td/table/tr[2]/td/table//tr')
        # response.xpath('/html/body/table/tbody/tr[2]/td/table/tr[2]/td/table/tr[1]/td[2]/a/text()').extract()

        for title in titleList:
            news_title = title.xpath('./td[2]/a/text()').extract()[0]
            news_url = response.urljoin(title.xpath('./td[2]/a/@href').extract()[0])
            news_date = title.xpath('./td[3]/text()').extract()[0].replace('[','').replace(']','').replace('.','-')
            request = scrapy.http.Request(news_url, callback=self.parse_newsContent)
            request.meta['news_title'] = news_title
            request.meta['news_date'] = news_date
            yield request


    #解析文章内容
    def parse_newsContent(self, response):
        datadate = datetime.datetime.strptime(response.meta['news_date'], '%Y-%m-%d')
        # datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y/%m/%d %H:%M:%S')
        # print response.url
        if response.xpath('.//table/tbody/tr/td/div[@class="info"]').extract() <> []:
            htmlContent = response.xpath('.//table/tbody/tr/td/div[@class="info"]').extract()[0]

            if len(htmlContent) < 20:
                print u'新闻可能不全，url为--->' + response.url
            else:
                item = Puok_mohurdItem()
                item['datadate'] = datadate
                item['news_type'] = ''
                item['news_title'] = response.meta['news_title']
                item['news_url'] = response.url
                item['image_url'] = ''
                item['update_dt'] = today
                item['html_news'] = htmlContent
                yield item
        else:
            print u'Xpath首次解析失败，url为--->' + response.url
            item = Puok_mohurdItem()
            item['datadate'] = datadate
            item['news_type'] = ''
            item['news_title'] = response.meta['news_title']
            item['news_url'] = response.url
            item['image_url'] = ''
            item['update_dt'] = today
            item['html_news'] = None
            yield item
        # htmlnews = response.xpath('//td[@class="content"]')[0].extract()
        # html_parser = lxml.html.HTMLParser(encoding='gb2312', remove_comments=True)
        # content_html_etree = lxml.html.fromstring(htmlnews, parser=html_parser)
        # lxml.etree.strip_elements(content_html_etree, 'iframe', 'script', 'style')
        # htmlnews = lxml.html.tostring(content_html_etree, encoding='utf-8').decode('utf-8')


