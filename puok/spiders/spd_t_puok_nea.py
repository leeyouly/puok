# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_neaItem
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

index = 1

#扑克财经需求--能源局通知和公告抓取
class PuokNEA(scrapy.Spider):
    name = "spd_t_puok_nea"
    start_urls = (
        'http://www.nea.gov.cn/',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'国家能源局')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_nea'])

        # url = 'http://www.nea.gov.cn/20140521_1449.pdf'
        # request = scrapy.http.FormRequest(url, callback=self.parse_title)
        # yield request

        for news_type in ['tz','gg']:
            if news_type == 'tz':
                sumPage = 3
            elif news_type == 'gg':
                sumPage = 3
            for page in range(1,sumPage,1):
                if page == 1:
                    titleurl = 'http://www.nea.gov.cn/policy/'+news_type+'.htm'
                else :
                    titleurl = 'http://www.nea.gov.cn/policy/'+news_type+'_'+str(page)+'.htm'

                request = scrapy.http.FormRequest(titleurl, callback=self.parse_title)
                request.meta['news_type'] = news_type
                yield request

    #解析文章标题以及url
    def parse_title(self, response):
        newsUl = response.xpath('/html/body/div[@class="content"]/div[@class="box01"]/ul')

        for newsList in newsUl:
            news = newsList.xpath('./li')
            for newsDetail in news:
                if newsDetail.xpath('./a/text()').extract() <>[]:
                # if news.xpath('./li/a/text()').extract() <>[]:
                    datadate = newsDetail.xpath('./span/text()').extract()[0]
                    newsTitle = newsDetail.xpath('./a/text()').extract()[0]
                    newsHref = newsDetail.xpath('./a/@href').extract()[0]
                    # print 'newsHref----> ' + newsHref
                    # print 'response.urljoin----> ' + response.urljoin(newsHref)
                    # print newsTitle
                    # newsContentURL = 'http://www.ndrc.gov.cn/xwzx/xwfb/'+newsHref.replace('./','')
                    request = scrapy.http.Request(newsHref, callback=self.parse_newsContent)
                    request.meta['datadate'] = datadate
                    request.meta['newsTitle'] = newsTitle
                    request.meta['newsContentURL'] = newsHref
                    request.meta['news_type'] = response.meta['news_type']
                    yield request
                else:
                    print u'未找到url'

    #解析文章内容
    def parse_newsContent(self, response):
        datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y-%m-%d')
        imageurl = ''
        newsTitle = response.meta['newsTitle']
        newsContentURL = response.meta['newsContentURL']

        contentStr = response.body
        #有一些公告就是pdf格式的，无法解析成html，用newstitle+newurl的方式存储在news_html中
        if 'PDF' in contentStr:
            global index
            print u'pdf第 ' + str(index) + u' 次打印'
            index = index + 1
            item = Puok_neaItem()
            item['datadate'] = datadate
            if response.meta['news_type'] == 'gg':
                item['news_type'] = u'公告'
            elif response.meta['news_type'] == 'tz':
                item['news_type'] = u'通知'
            item['news_title'] = newsTitle
            item['news_content'] = u''
            item['news_html'] = newsTitle + ' ' + response.url
            item['news_contenturl'] = newsContentURL
            item['news_imageurl'] = imageurl
            item['update_dt'] = datetime.datetime.now()
            yield item
        else:
            news_html= response.xpath('/html/body/div["main-colum"]/div[@class="channel-page"]/'
                                      'div[@class="article-box"]/div[@class="article-content"]')
            if len(news_html) < 1:
                news_html = response.xpath('//*[@id="tex"]')
                if len(news_html) < 1:
                    print u'未解析到文章内容,url ---> ' + response.url

            news_html = news_html.extract()[0]
            html_parser = lxml.html.HTMLParser(encoding='gb2312', remove_comments=True)
            content_html_etree = lxml.html.fromstring(news_html, parser=html_parser)
            lxml.etree.strip_elements(content_html_etree, 'iframe', 'script', 'style')
            news_html = lxml.html.tostring(content_html_etree, encoding='utf-8').decode('utf-8')
            spd_t_puok_nea.py
            item = Puok_neaItem()
            item['datadate'] = datadate
            if response.meta['news_type'] == 'gg':
                item['news_type'] = u'公告'
            elif response.meta['news_type'] == 'tz':
                item['news_type'] = u'通知'
            item['news_title'] = newsTitle
            item['news_content'] = u''
            item['news_html'] = news_html
            item['news_contenturl'] = newsContentURL
            item['news_imageurl'] = imageurl
            item['update_dt'] = datetime.datetime.now()
            yield item

        # newsContent = u''
        # for paragraph in htmlContent:
        #     #//text() 两个/的text()可以得到该标签下所有的文本
        #     paraList = paragraph.xpath('.//text()').extract()
        #     # imageurl = paragraph.xpath('./img/@src').extract() + ', '+ imageurl
        #     imageurllist = paragraph.xpath('./img/@src').extract()
        #     if imageurllist <> []:
        #         imageurl = ';\n'.join(imageurllist).\
        #                    replace('./','http://www.ndrc.gov.cn/xwzx/xwfb/'+datadate.strftime('%Y%m')+'/')\
        #                    + ';\n' + imageurl
        #     contentStr = u''
        #     for para in paraList:
        #         #处理字符乱码的问题
        #         contentStr = contentStr + para.replace(u'\xa0',u'')
        #     newsContent = newsContent + contentStr + '\n'

        # htmltext = response.xpath('//*[@id="zoom"]/div[@class="TRS_Editor"]/p').extract()
        # # 如果获取的内容为空或者文章内容小于1段(包括回车也算一段)，则也认为未获取到文章。那么从div标签取
        # if len(htmltext) < 1:
        #     htmltext = response.xpath('//*[@id="zoom"]/div[@class="TRS_Editor"]/div').extract()
        #     if len(htmlContent) < 1:
        #         htmltext = response.xpath('//*[@id="zoom"]/div[@class="TRS_Editor"]').extract()
        #
        # htmlnews = '\n'.join(htmltext).replace('src="./','src="http://www.ndrc.gov.cn/xwzx/xwfb/'+datadate.strftime('%Y%m')+'/')

        # htmlnews = response.xpath('//td[@class="content"]')[0].extract()
        # html_parser = lxml.html.HTMLParser(encoding='gb2312', remove_comments=True)
        # content_html_etree = lxml.html.fromstring(htmlnews, parser=html_parser)
        # lxml.etree.strip_elements(content_html_etree, 'iframe', 'script', 'style')
        # htmlnews = lxml.html.tostring(content_html_etree, encoding='utf-8').decode('utf-8')



