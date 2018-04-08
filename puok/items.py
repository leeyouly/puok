# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class Puok_SteelItem(scrapy.Item):
    datadate = scrapy.Field()
    data_type = scrapy.Field()
    news_contents = scrapy.Field()
    pageid = scrapy.Field()


class Puok_GangguItem(scrapy.Item):
    datadate = scrapy.Field()
    data_type = scrapy.Field()
    news_contents = scrapy.Field()
    pageid = scrapy.Field()


class Puok_ndrcItem(scrapy.Item):
    datadate = scrapy.Field()
    newstitle = scrapy.Field()
    newscontent = scrapy.Field()
    htmlnews = scrapy.Field()
    newscontenturl = scrapy.Field()
    imageurl = scrapy.Field()


class Puok_mepItem(scrapy.Item):
    datadate = scrapy.Field()
    newstype = scrapy.Field()
    newstitle = scrapy.Field()
    newscontent = scrapy.Field()
    htmlnews = scrapy.Field()
    newscontenturl = scrapy.Field()
    imageurl = scrapy.Field()


class Puok_chinaisaItem(scrapy.Item):
    datadate = scrapy.Field()
    news_type = scrapy.Field()
    news_title = scrapy.Field()
    news_contentframeurl = scrapy.Field()
    news_contentrealurl = scrapy.Field()
    image_url = scrapy.Field()
    update_dt = scrapy.Field()
    html_news = scrapy.Field()


class Puok_mohurdItem(scrapy.Item):
    datadate = scrapy.Field()
    news_type = scrapy.Field()
    news_title = scrapy.Field()
    news_url = scrapy.Field()
    image_url = scrapy.Field()
    update_dt = scrapy.Field()
    html_news = scrapy.Field()

class Puok_tradeNoticeItem(scrapy.Item):
    datadate = scrapy.Field()
    bourse = scrapy.Field()
    news_type = scrapy.Field()
    news_title = scrapy.Field()
    news_url = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()
    html_news = scrapy.Field()

class Puok_chinaisaSortpriceItem(scrapy.Item):
    datadate = scrapy.Field()
    page_date = scrapy.Field()
    page_sort = scrapy.Field()
    mainsize = scrapy.Field()
    mainsort = scrapy.Field()
    index_name = scrapy.Field()
    price = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()

class Puok_chinaisaPartpriceItem(scrapy.Item):
    datadate = scrapy.Field()
    page_date = scrapy.Field()
    # page_title = scrapy.Field()
    mainsort = scrapy.Field()
    mainsize = scrapy.Field()
    part = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()


class Puok_neaItem(scrapy.Item):
    datadate = scrapy.Field()
    news_type = scrapy.Field()
    news_title = scrapy.Field()
    news_content = scrapy.Field()
    news_html = scrapy.Field()
    news_contenturl = scrapy.Field()
    news_imageurl = scrapy.Field()
    update_dt = scrapy.Field()


class Puok_csrcItem(scrapy.Item):
    datadate = scrapy.Field()
    news_title = scrapy.Field()
    news_content = scrapy.Field()
    news_html = scrapy.Field()
    news_contenturl = scrapy.Field()
    news_imageurl = scrapy.Field()
    update_dt = scrapy.Field()

class Puok_cansiItem(scrapy.Item):
    datadate = scrapy.Field()
    index_name = scrapy.Field()
    world = scrapy.Field()
    china = scrapy.Field()
    korea = scrapy.Field()
    japan = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()


class Puok_96369Item(scrapy.Item):
    datadate = scrapy.Field()
    news_title = scrapy.Field()
    news_content = scrapy.Field()
    news_html = scrapy.Field()
    news_contenturl = scrapy.Field()
    news_imageurl = scrapy.Field()
    update_dt = scrapy.Field()


class Puok_statsItem(scrapy.Item):
    datadate = scrapy.Field()
    news_title = scrapy.Field()
    news_content = scrapy.Field()
    news_html = scrapy.Field()
    news_contenturl = scrapy.Field()
    news_imageurl = scrapy.Field()
    update_dt = scrapy.Field()


class Puok_jin10Item(scrapy.Item):
    datadate = scrapy.Field()
    data_type = scrapy.Field()
    news_contents = scrapy.Field()
    pageid = scrapy.Field()
    update_dt = scrapy.Field()