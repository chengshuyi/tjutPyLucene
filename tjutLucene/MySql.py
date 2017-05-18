import pymysql.cursors

class MySql:
    table_name='webpage'

    _id='id'
    url = 'url'
    title = 'title'
    keyword = 'keyword'
    content = 'content'
    last_modified = 'last_modified'
    next_scrawl_time = 'next_scrawl_time'
    isUpdate = 'isUpdate'
    isIndex = 'isIndex'

    conn=''

    def __init__(self,db_name='test',user='root',password='123456'):

        # connect the mysql
        self.conn=pymysql.connect(  host='localhost',
                                    user=user,
                                    password=password,
                                    db=db_name,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    def selectUnIndexCursor(self):
        sql = 'select * from '+self.table_name+' where '+self.isIndex+'=0'
        cursor=self.conn.cursor()
        num=cursor.execute(sql)
        return num,cursor

    def selectUpdateCursor(self):
        sql = 'select * from '+self.table_name+' where '+self.isUpdate+'=1'
        cursor=self.conn.cursor()
        num=cursor.execute(sql)
        return num,cursor

    def updateAllIsUpdate(self):
        sql='UPDATE '+self.table_name+' SET '+self.isUpdate+'=0'
        with self.conn.cursor()  as cursor:
            cursor.execute(sql)
        self.conn.commit()

    def updateAllIsIndex(self):
        sql='UPDATE '+self.table_name+' SET '+self.isIndex+'=1'
        with self.conn.cursor()  as cursor:
            cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()