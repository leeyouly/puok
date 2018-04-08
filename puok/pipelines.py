# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from puok.data import ImportPuok_SteelStorage,ImportPuok_GangguStorage,ImportPuok_ndrcStorage,\
    ImportPuok_mepStorage,ImportPuok_chinaisaStorage,ImportPuok_mohurdStorage,ImportPuok_tradeNoticeStorage,\
    ImportPuok_chinaisaSortpriceStorage, ImportPuok_chinaisaPartpriceStorage,ImportPuok_neaStorage,ImportPuok_csrcStorage,\
    ImportPuok_cansiStorage,ImportPuok_96369Storage,ImportPuok_statsStorage,ImportPuok_jin10Storage
from puok.items import Puok_SteelItem,Puok_GangguItem,Puok_ndrcItem,Puok_mepItem,Puok_chinaisaItem,\
    Puok_mohurdItem,Puok_tradeNoticeItem,Puok_chinaisaSortpriceItem,Puok_chinaisaPartpriceItem,Puok_neaItem,Puok_csrcItem,\
    Puok_cansiItem,Puok_96369Item,Puok_statsItem,Puok_jin10Item
from scrapy.utils.project import get_project_settings

class PuokPipeline(object):
    def process_item(self, item, spider):
        return item


class Puok_SteelPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_SteelStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_SteelItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class Puok_GangguPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_GangguStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_GangguItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class Puok_ndrcPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_ndrcStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_ndrcItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class Puok_mepPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_mepStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_mepItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class Puok_chinaisaPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_chinaisaStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_chinaisaItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class Puok_mohurdPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_mohurdStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_mohurdItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class Puok_tradeNoticePipleline(object):
    def __init__(self):
        self.storage = ImportPuok_tradeNoticeStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_tradeNoticeItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class Puok_chinaisaSortpricePipleline(object):
    def __init__(self):
        self.storage = ImportPuok_chinaisaSortpriceStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_chinaisaSortpriceItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class Puok_chinaisaPartpricePipleline(object):
    def __init__(self):
        self.storage = ImportPuok_chinaisaPartpriceStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_chinaisaPartpriceItem):
            if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

#国家能源局
class Puok_neaPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_neaStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_neaItem):
            if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class Puok_csrcPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_csrcStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_csrcItem):
            if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class Puok_cansiPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_cansiStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_cansiItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class Puok_96369Pipleline(object):
    def __init__(self):
        self.storage = ImportPuok_96369Storage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_96369Item):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class Puok_statsPipleline(object):
    def __init__(self):
        self.storage = ImportPuok_statsStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_statsItem):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class Puok_jin10Pipleline(object):
    def __init__(self):
        self.storage = ImportPuok_jin10Storage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, Puok_jin10Item):
            # if not self.storage.exist(item):
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')

        return item