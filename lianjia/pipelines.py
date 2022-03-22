# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from hashlib import md5
from lianjia.settings import *


class LianjiaPipeline:
    def process_item(self, item, spider):
        return item


class MySQLStoreCnblogsPipeline:
    # pipeline默认调用
    def process_item(self, item, spider):
        # conn = pymysql.connect(host='127.0.0.1', user='root', password='123456',
        #                        db='scrapy_home', charset='utf8', port=3306, use_unicode=False)
        conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWD,
                               db=MYSQL_DBNAME, charset='utf8', port=MYSQL_PORT, use_unicode=False)
        linkmd5id = get_linkmd5id(item)
        cursor = conn.cursor()
        get_sql = 'SELECT * from lianjia_spider WHERE linkmd5id=%s'
        res = cursor.execute(get_sql, linkmd5id)
        conn.commit()
        try:
            if res:
                update_sql = "update lianjia_spider set resblock_price_url=%s, resblock_name=%s, resblock_type=%s, " \
                             "resblock_status=%s, resblock_location=%s, resblock_room=%s, resblock_area=%s, " \
                             "resblock_tag=%s, resblock_price=%s, resblock_second=%s, detail_url=%s where " \
                             "linkmd5id=%s;"
                cursor.execute(update_sql, [item['resblock_price_url'], item['resblock_name'],
                                            item['resblock_type'], item['resblock_status'],
                                            item['resblock_location'], item['resblock_room'],
                                            item['resblock_area'], str(item['resblock_tag']),
                                            item['resblock_price'], item['resblock_second'],
                                            item['detail_url'], linkmd5id])
                conn.commit()
            else:
                insert_sql = "insert into lianjia_spider(resblock_price_url,resblock_name, resblock_type," \
                             "resblock_status,resblock_location, resblock_room, resblock_area, resblock_tag, " \
                             "resblock_price, resblock_second,detail_url, linkmd5id) values(%s,%s,%s,%s,%s,%s,%s,%s," \
                             "%s,%s,%s,%s); "
                cursor.execute(insert_sql, [item['resblock_price_url'], item['resblock_name'],
                                            item['resblock_type'], item['resblock_status'],
                                            item['resblock_location'], item['resblock_room'],
                                            item['resblock_area'], item['resblock_tag'],
                                            item['resblock_price'], item['resblock_second'],
                                            item['detail_url'], linkmd5id])
                conn.commit()
        except Exception as e:
            conn.rollback()
            conn.close()
        conn.close()


# 获取url的md5编码
def get_linkmd5id(item):
    # url进行md5处理，为避免重复采集设计
    return md5(item['detail_url'].encode("utf8")).hexdigest()
