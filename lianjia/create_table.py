import pymysql

from lianjia.settings import *
def create_table():
    # 连接本地数据库
    db = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWD,
                         db=MYSQL_DBNAME, charset='utf8', port=MYSQL_PORT, use_unicode=False)

    # 创建游标
    cursor = db.cursor()
    sql = """
        CREATE TABLE lianjia_spider (
  id int primary key not null AUTO_INCREMENT,
  resblock_price_url VARCHAR (255),
  resblock_name VARCHAR (255),
  resblock_type VARCHAR (255),
  resblock_status VARCHAR(500),
  resblock_location VARCHAR (255),
  resblock_room VARCHAR (255),
  resblock_area VARCHAR(255),
  resblock_tag VARCHAR(255),
  resblock_price VARCHAR (255),
  resblock_second VARCHAR (255),
  detail_url VARCHAR (255)
)
    """

    try:
        insert_sql = """insert into scrapy_home(linkmd5id, resblock_price_url, resblock_name, resblock_type, resblock_status,
                            resblock_location, resblock_room, resblock_area, resblock_tag, resblock_price,
                            resblock_second, detail_url) 
                            values(linkmd5id, item['resblock_price_url'], item['resblock_name'], item['resblock_type'], item['resblock_status'],
                              item['resblock_location'], item['resblock_room'], item['resblock_area'], item['resblock_tag'],item['resblock_price'],
                              item['resblock_second'], item['detail_url'])"""
        cursor.execute(insert_sql)
        db.commit()
        # 执行SQL语句
        # cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s" % e)
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        db.close()


def main():
    create_table()


if __name__ == "__main__":
    main()