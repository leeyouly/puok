from spiderlib.data import DataStorage
import PyDB

class ImportPuok_SteelStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_STEEL'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate"),
            PyDB.IntField("pageid", is_key=True),
            PyDB.StringField("data_type"),
            PyDB.StringField("news_contents"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_GangguStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_GANGGU'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate"),
            PyDB.IntField("pageid", is_key=True),
            PyDB.StringField("data_type"),
            PyDB.StringField("news_contents"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()

class ImportPuok_ndrcStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_NDRC'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate"),
            PyDB.StringField("newstitle"),
            PyDB.StringField("newscontent"),
            PyDB.StringField("htmlnews"),
            PyDB.StringField("imageurl"),
            PyDB.StringField("newscontenturl", is_key=True),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_mepStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_MEP'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate"),
            PyDB.StringField("newstype"),
            PyDB.StringField("newstitle"),
            PyDB.StringField("imageurl"),
            PyDB.StringField("newscontenturl", is_key=True),
            PyDB.StringField("newscontent"),
            PyDB.StringField("htmlnews"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_chinaisaStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_CHINAISA'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("news_type", is_key=True),
            PyDB.StringField("news_title"),
            PyDB.StringField("news_contentframeurl"),
            PyDB.StringField("news_contentrealurl", is_key=True),
            PyDB.StringField("image_url"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("html_news"),

        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_mohurdStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_MOHURD'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("news_type"),
            PyDB.StringField("news_title"),
            PyDB.StringField("news_url", is_key=True),
            PyDB.StringField("image_url"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("html_news"),

        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_tradeNoticeStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_TRADENOTICE'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("bourse"),
            PyDB.StringField("news_type"),
            PyDB.StringField("news_title"),
            PyDB.StringField("news_url", is_key=True),
            PyDB.DateField("update_dt"),
            PyDB.StringField("source"),
            PyDB.StringField("html_news"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_chinaisaSortpriceStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_CHINAISA_SORTPRICE'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("page_date"),
            PyDB.StringField("page_sort"),
            PyDB.StringField("mainsort", is_key=True),
            PyDB.StringField("mainsize", is_key=True),
            PyDB.StringField("index_name", is_key=True),
            PyDB.StringField("price"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("source"),
        ])

    def save_or_update(self, item):
        # self.db.save_or_update(self.table_name, item)
        self.db.save(self.table_name, item)
        self.db.commit()


class ImportPuok_chinaisaPartpriceStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_CHINAISA_PARTPRICE'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("page_date"),
            # PyDB.StringField("page_sort"),
            PyDB.StringField("mainsort", is_key=True),
            PyDB.StringField("mainsize", is_key=True),
            PyDB.StringField("part", is_key=True),
            PyDB.StringField("price"),
            PyDB.StringField("unit"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("source"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_neaStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_NEA'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate"),
            PyDB.StringField("news_type"),
            PyDB.StringField("news_title"),
            PyDB.StringField("news_content"),
            PyDB.StringField("news_contenturl"),
            PyDB.StringField("news_html"),
            PyDB.StringField("news_imageurl"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("news_contenturl", is_key=True),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_csrcStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_CSRC'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate"),
            PyDB.StringField("news_title"),
            PyDB.StringField("news_content"),
            PyDB.StringField("news_contenturl"),
            PyDB.StringField("news_html"),
            PyDB.StringField("news_imageurl"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("news_contenturl", is_key=True),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_cansiStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_CANSI'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("datadate", is_key=True),
            PyDB.StringField("index_name", is_key=True),
            PyDB.StringField("world"),
            PyDB.StringField("china"),
            PyDB.StringField("korea"),
            PyDB.StringField("japan"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("source"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_96369Storage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_96369'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate"),
            PyDB.StringField("news_title"),
            PyDB.StringField("news_content"),
            PyDB.StringField("news_contenturl"),
            PyDB.StringField("news_html"),
            PyDB.StringField("news_imageurl"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("news_contenturl", is_key=True),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()

class ImportPuok_statsStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_STATS'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("datadate"),
            PyDB.StringField("news_title"),
            PyDB.StringField("news_content"),
            PyDB.StringField("news_contenturl"),
            PyDB.StringField("news_html"),
            PyDB.StringField("news_imageurl"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("news_contenturl", is_key=True),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportPuok_jin10Storage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_PUOK_JIN10'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.IntField("pageid", is_key=True),
            PyDB.StringField("data_type"),
            PyDB.StringField("news_contents"),
            PyDB.DateField("update_dt"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()