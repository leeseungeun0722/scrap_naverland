from unittest.mock import DEFAULT
import mysql.connector
from itemadapter import ItemAdapter
from datetime import datetime

class NaverLandPipeline(object):
    
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'naverland',
            user = 'root',
            password = 'pw',
            charset = 'utf8',
            port = '3306',
            auth_plugin='mysql_native_password',
            database = 'Naver_land',
            use_unicode=True
        )
        self.curr = self.conn.cursor()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter.get('dong_Name')
        adapter.get('DONG_NAME')

        for i in adapter['DONG_NAME']:
            DONG = i
            self.curr.execute(f"CREATE TABLE IF NOT EXISTS {DONG} (dong VARCHAR(30) NOT NULL, apart VARCHAR(60) NOT NULL,tradetype VARCHAR(60) NOT NULL, pyeong VARCHAR(60) NOT NULL,floor SMALLINT(5) NOT NULL ,year SMALLINT(5) NOT NULL, month TINYINT(4) NOT NULL, date TINYINT(4) NOT NULL, price INT(50) NOT NULL, monthly VARCHAR(50) NOT NULL, UPDATE_TIME DATETIME NOT NULL)")  
            sql = (f"INSERT INTO {DONG} VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            
            if DONG == adapter['dong_Name']:
            
                val = (adapter['dong_Name'],adapter['apartment_Name'],item['type_List'],item['pyeongName'],item['floor'],item['year'],item['month'],item['date'],item['price'],item['monthly'],item['UPDATETIME'])
                self.curr.execute(sql,val)
                self.conn.commit()
    
        return item
