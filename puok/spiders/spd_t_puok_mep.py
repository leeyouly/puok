# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_mepItem
import puok.settings as settings
import cx_Oracle
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


#扑克财经需求--环保部新闻抓取
class PuokSteel(scrapy.Spider):
    name = "spd_t_puok_mep"
    allowed_domains = ["mep.gov.cn"]
    start_urls = (
        'http://www.mep.gov.cn',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'中华人名共和国环保部')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_mep'])

        titletypeDict = {'jjwm':u'聚焦重污染天气', 'zcfgjd':u'政策法规解读'}
        # titletypeDict = {'zcfgjd':u'政策法规解读'}

        for key in titletypeDict:
            for page in range(3):
            # for page in range(0,1,1):
                if (page > 7) and (key =='zcfgjd'):
                    continue
                if page == 0:
                    titleurl = 'http://www.mep.gov.cn/xxgk/'+ key +'/index.shtml'
                else :
                    titleurl = 'http://www.mep.gov.cn/xxgk/'+ key +'/index_'+str(page)+'.shtml'
                request = scrapy.http.FormRequest(titleurl, callback=self.parse_title)
                request.meta['titletype'] = titletypeDict[key]
                yield request

    #解析标题
    def parse_title(self, response):
        titletype = response.meta['titletype']
        newsList = response.xpath('//div[@class="main"]/div[@class="main_rt"]/div[@class="main_rt_list"]/ul/li')

        for news in newsList:
            # if news.xpath('./font/text()').extract() <>[]:
            datadate = news.xpath('./div/span/text()').extract()[0]
            newsTitle = news.xpath('./div/a/@title').extract()[0]
            newsHref = news.xpath('./div/a/@href').extract()[0]
            newsContentURL = ''
            # if titletype == u'聚焦重污染天气':
            if 'http' in newsHref:
                newsContentURL = newsHref
            else:
                if './20' in newsHref:
                    newsContentURL = 'http://www.mep.gov.cn/xxgk/zcfgjd/' + newsHref.replace('./','')
                elif '../hjyw' in newsHref:
                    newsContentURL = 'http://www.mep.gov.cn/xxgk/' + newsHref.replace('../hjyw', 'hjyw')
                else:
                    newsContentURL = 'http://www.mep.gov.cn/' + newsHref.replace('../','')

            # newsContentURL = 'http://www.mep.gov.cn/gkml/hbb/qt/' + '20' + re.findall('/20(.+)', newsHref)[0]
            request = scrapy.http.Request(newsContentURL, callback=self.parse_newsContent)
            request.meta['datadate'] = datadate
            request.meta['newsTitle'] = newsTitle
            request.meta['newsContentURL'] = newsContentURL
            request.meta['titletype'] = titletype
            yield request


    #解析文章内容
    def parse_newsContent(self, response):
        datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y-%m-%d')
        # datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y/%m/%d %H:%M:%S')
        newsTitle = response.meta['newsTitle']
        newsContentURL = response.meta['newsContentURL']
        #网页中的图片是相对路径，此处把相对路径补全
        imageurlStrat = re.findall('(.+)/20',newsContentURL)[0]+'/'
        titletype = response.meta['titletype']
        imageurl = ''
        newsContent = u''
        if titletype == u'聚焦重污染天气':
            #首先从p标签下获取文章内容
            htmlContent = response.xpath('//*[@id="ContentRegion"]/div/div/p')
            if htmlContent == []:
                htmlContent = response.xpath('//*[@id="ContentRegion"]/div/p')
                if htmlContent == []:
                    htmlContent = response.xpath('//*[@id="ContentRegion"]/p')
                    if htmlContent == []:
                        htmlContent = response.xpath('//*[@id="ContentRegion"]')

            for paragraph in htmlContent:
                imageurllist = paragraph.xpath('./img/@src').extract()
                if imageurllist <> []:
                    imageurl = ';\n'.join(imageurllist).replace('./',imageurlStrat + datadate.strftime('%Y%m') + '/')\
                                + ';\n' + imageurl
                #//text() 两个/的text()可以得到该标签下所有的文本
                paraList = paragraph.xpath('.//text()').extract()
                contentStr = u''
                for para in paraList:
                    #处理字符乱码的问题
                    contentStr = contentStr + para.replace(u'\xa0',u'')
                newsContent = newsContent + contentStr + '\n'

            #环保部网站新闻部分架构非常混乱，文章可能出现在如下各种标签里，所以做多重处理
            htmltext = response.xpath('//*[@id="ContentRegion"]/div/div/p').extract()
            if htmltext == []:
                htmltext = response.xpath('//*[@id="ContentRegion"]/div/p').extract()
                if htmltext == []:
                    htmltext = response.xpath('//*[@id="ContentRegion"]/p').extract()
                    if htmltext == []:
                        htmltext = response.xpath('//*[@id="ContentRegion"]').extract()
                    elif htmltext == []:
                        htmltext = []
            htmlnews = ''.join(htmltext).replace('src="./',imageurlStrat + datadate.strftime('%Y%m')+'/')

        else:
            #xpath解析新闻内容，因环保部新闻的内容位置特别不规范，所以基本列举了可能出现文章内容的所有位置，
            #尽可能按照能精确查找的方式优先匹配，比如//*[@id="ContentRegion"]/text()肯定能解析到，
            #但优先匹配//*[@id="ContentRegion"]/div/div/p和//*[@id="ContentRegion"]/div/p这两类标签
            #每一个if层级的原则是这个标签取不到，就忘里再取一层
            # (当然这个写发法不太好，逻辑看着十分混乱。可以考虑用一个list，装载所有xpath的情况，
            # 用一个for循环来分别解析直到解析出来内容不为空，先这么做，后期有需要再改)
            htmlContent = response.xpath('//*[@id="ContentRegion"]/div//p')
            if htmlContent == []:
                htmlContent = response.xpath('//*[@id="ContentRegion"]/div/p')
                if htmlContent == []:
                    htmlContent = response.xpath('//*[@id="ContentRegion"]/p')
                    if htmlContent == []:
                        htmlContent = response.xpath('//*[@id="ContentRegion"]')
                        if htmlContent == []:
                            #另一种不同类型的网页解析
                            htmlContent = response.xpath('.//div[@class="TRS_Editor"]/p')
                            # 如果获取的内容为空或者文章内容小于1段(包括回车也算一段)，则也认为未获取到文章。那么从div标签取
                            if len(htmlContent) < 1:
                                htmlContent = response.xpath('.//div[@class="TRS_Editor"]/div')
                                if len(htmlContent) < 1:
                                    htmlContent = response.xpath('.//div[@class="TRS_Editor"]')
                                    if len(htmlContent) < 1:
                                        htmlContent = response.xpath('.//div[@class="wzxq_neirong2"]/p')
                                        if len(htmlContent) < 1:
                                            htmlContent = response.xpath('.//div[@class="wzxq_neirong2"]')
                                        elif htmlContent == []:
                                            htmlContent = []
            #处理抽取的网页文本内容
            for paragraph in htmlContent:
                imageurllist = paragraph.xpath('./img/@src').extract()
                if imageurllist <> []:
                    imageurl = ';\n'.join(imageurllist).replace('./', imageurlStrat + datadate.strftime('%Y%m') + '/') \
                               + ';\n' + imageurl
                #//text() 两个/的text()可以得到该标签下所有的文本
                paraList = paragraph.xpath('.//text()').extract()
                contentStr = u''
                #新闻文本返回为list，需拼接为一段，另外也处理下乱码相关的问题
                for para in paraList:
                    #处理字符乱码的问题
                    contentStr = contentStr + para.replace(u'\xa0',u'')
                newsContent = newsContent + contentStr + '\n'

            #环保部网站新闻部分架构非常混乱，文章可能出现在如下各种标签里，所以做多重处理 具体参见上文注释
            htmltext = response.xpath('//*[@id="ContentRegion"]/div/div/p').extract()
            if htmltext == []:
                htmltext = response.xpath('//*[@id="ContentRegion"]/div/p').extract()
                if htmltext == []:
                    htmltext = response.xpath('//*[@id="ContentRegion"]/p').extract()
                    if htmltext == []:
                        htmltext = response.xpath('//*[@id="ContentRegion"]').extract()
                        if htmltext == []:
                            #另一种不同类型的网页解析
                            htmltext = response.xpath('.//div[@class="TRS_Editor"]/p').extract()
                            # 如果获取的内容为空或者文章内容小于1段(包括回车也算一段)，
                            # 则也认为未获取到文章。那么从div标签取
                            if len(htmltext) < 1:
                                htmltext = response.xpath('.//div[@class="TRS_Editor"]/div').extract()
                                if len(htmltext) < 1:
                                    htmltext = response.xpath('.//div[@class="TRS_Editor"]').extract()
                                    if len(htmltext) < 1:
                                        htmltext = response.xpath('.//div[@class="wzxq_neirong2"]/p').extract()
                                        if len(htmlContent) < 1:
                                            htmltext = response.xpath('.//div[@class="wzxq_neirong2"]')
                                        elif htmltext == []:
                                            htmltext = []

            htmlnews = ''.join(htmltext).replace('oldsrc="',imageurlStrat + datadate.strftime('%Y%m')+'/').replace('jpg"','jpg').replace('png"','png')

        #写文件和存数据库用的Item
        item = Puok_mepItem()
        item['datadate'] = datadate
        item['newstype'] = titletype
        item['newstitle'] = newsTitle
        item['newscontenturl'] = newsContentURL
        item['newscontent'] = newsContent
        item['htmlnews'] = htmlnews
        item['imageurl'] = imageurl
        yield item

