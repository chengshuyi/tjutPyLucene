import pymysql
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

	conn=''

	def __init__(self,db_name='test',user='root',password='123456'):

		# connect the mysql
		self.conn=pymysql.connect(	host='localhost',
								   	user=user,
									password=password,
									db=db_name,
									charset='utf8mb4',
									cursorclass=pymysql.cursors.DictCursor)


	
	def buildHashForUrl(self):
		sql= 'SELECT * FROM '+self.table_name
		hashUrl={}

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			for i in range(int(cursor.rowcount)):
				oneItem = cursor.fetchone()
				hashUrl[oneItem[self.url]]= {
						self._id:oneItem[self._id],
						self.last_modified:int(oneItem[self.last_modified]),
						self.next_scrawl_time:int(oneItem[self.next_scrawl_time])
					}
		return hashUrl

	"""
	check  pre_last_modified & last_modified
	"""
	def update(self,item):
		sql ='UPDATE '+self.table_name+' SET '+self.title+'=%s,'+self.keyword+'=%s,'+self.content+'=%s,'+self.last_modified+'=%s,'+self.isUpdate+'=%s,'+self.next_scrawl_time+'=%s WHERE '+self._id+'=%s'
		with self.conn.cursor() as cursor:
			cursor.execute(sql,(item[self.title],item[self.keyword],item[self.content],str(item[self.last_modified],str(1),str(item[self.next_scrawl_time],str(item['_id'])))))
		self.conn.commit()

	def insert(self,item):

		sql	= 'INSERT '+self.table_name+' ('+','.join([self._id,self.url,self.title,self.keyword,self.content,self.last_modified,self.next_scrawl_time])+') VALUES (%s,%s,%s,%s,%s,%s,%s)'
		with self.conn.cursor() as cursor:
			cursor.execute(sql,(item['_id'],item[self.url],item[self.title],item[self.keyword],item[self.content],str(item[self.last_modified]),str(item[self.next_scrawl_time]))) 
		self.conn.commit()


	def getMaxId(self):
		ret = 0
		sql = 'SELECT max('+self._id +') FROM '+self.table_name
		try:
			with self.conn.cursor() as cursor:
				cursor.execute(sql)
				ret = int(cursor.fetchone()['max(id)'])
		except Exception,e:
			print Exception,":",e
		return ret