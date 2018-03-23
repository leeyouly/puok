# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_ndrcItem
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



#扑克财经需求--发改委抓取
class PuokNDRC(scrapy.Spider):
    name = "spd_t_puok_ndrc"
    start_urls = (
        'http://www.ndrc.gov.cn/xwzx/xwfb/index.html',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'发改委新闻发布中心')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_ndrc'])


        for page in range(3):
            if page == 0:
                titleurl = 'http://www.ndrc.gov.cn/xwzx/xwfb/index.html'
            else :
                titleurl = 'http://www.ndrc.gov.cn/xwzx/xwfb/index_'+str(page)+'.html'

            request = scrapy.http.FormRequest(titleurl, callback=self.parse_title)
            # request.meta['pagetype'] = pagetypeDict[key]
            yield request

    #解析文章标题以及url
    def parse_title(self, response):
        # contentStr = response.body
        newsList = response.xpath('//*[@id="out-content"]/div[@class="index_wrapper1 '
                                    'screen_width clearfix"]/div[@class="cell_two1 "]/'
                                    'div[@class="cell_two1_Right "]/div/ul[@class="list_02 clearfix"]/li')

        for news in newsList:
            if news.xpath('./font/text()').extract() <>[]:
                datadate = news.xpath('./font/text()').extract()[0]
                newsTitle = news.xpath('./a/text()').extract()[0]
                newsHref = news.xpath('./a/@href').extract()[0]
                newsContentURL = 'http://www.ndrc.gov.cn/xwzx/xwfb/'+newsHref.replace('./','')
                request = scrapy.http.Request(newsContentURL, callback=self.parse_newsContent)
                request.meta['datadate'] = datadate
                request.meta['newsTitle'] = newsTitle
                request.meta['newsContentURL'] = newsContentURL
                yield request

    #解析文章内容
    def parse_newsContent(self, response):
        datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y/%m/%d')
        # datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y/%m/%d %H:%M:%S')
        # datadate = response.meta['datadate']
        imageurl = ''
        newsTitle = response.meta['newsTitle']
        newsContentURL = response.meta['newsContentURL']
        #首先从p标签下获取文章内容
        htmlContent = response.xpath('//*[@id="zoom"]/div[@class="TRS_Editor"]/p')
        #如果获取的内容为空或者文章内容小于3段(包括回车也算一段)，则也认为未获取到文章。那么从div标签取
        if len(htmlContent) < 1:
            htmlContent = response.xpath('//*[@id="zoom"]/div[@class="TRS_Editor"]/div')
            if len(htmlContent) < 1:
                htmlContent = response.xpath('//*[@id="zoom"]/div[@class="TRS_Editor"]')

        newsContent = u''
        for paragraph in htmlContent:
            #//text() 两个/的text()可以得到该标签下所有的文本
            paraList = paragraph.xpath('.//text()').extract()
            # imageurl = paragraph.xpath('./img/@src').extract() + ', '+ imageurl
            imageurllist = paragraph.xpath('./img/@src').extract()
            if imageurllist <> []:
                imageurl = ';\n'.join(imageurllist).\
                           replace('./','http://www.ndrc.gov.cn/xwzx/xwfb/'+datadate.strftime('%Y%m')+'/')\
                           + ';\n' + imageurl
            contentStr = u''
            for para in paraList:
                #处理字符乱码的问题
                contentStr = contentStr + para.replace(u'\xa0',u'')
            newsContent = newsContent + contentStr + '\n'

        htmltext = response.xpath('//*[@id="zoom"]/div[@class="TRS_Editor"]/p').extract()
        # 如果获取的内容为空或者文章内容小于1段(包括回车也算一段)，则也认为未获取到文章。那么从div标签取
        if len(htmltext) < 1:
            htmltext = response.xpath('//*[@id="zoom"]/div[@class="TRS_Editor"]/div').extract()
            if len(htmlContent) < 1:
                htmltext = response.xpath('//*[@id="zoom"]/div[@class="TRS_Editor"]').extract()

        htmlnews = '\n'.join(htmltext).replace('src="./','src="http://www.ndrc.gov.cn/xwzx/xwfb/'+datadate.strftime('%Y%m')+'/')

        # htmlnews = response.xpath('//td[@class="content"]')[0].extract()
        # html_parser = lxml.html.HTMLParser(encoding='gb2312', remove_comments=True)
        # content_html_etree = lxml.html.fromstring(htmlnews, parser=html_parser)
        # lxml.etree.strip_elements(content_html_etree, 'iframe', 'script', 'style')
        # htmlnews = lxml.html.tostring(content_html_etree, encoding='utf-8').decode('utf-8')

        item = Puok_ndrcItem()
        item['datadate'] = datadate
        item['newstitle'] = newsTitle
        item['newscontent'] = newsContent
        item['htmlnews'] = htmlnews
        item['newscontenturl'] = newsContentURL
        item['imageurl'] = imageurl
        yield item

