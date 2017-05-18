#coding:utf-8
from BuildIndex import BuildIndex
from MySql import MySql
import pymysql.cursors

index_dir='.././data/index'
bi = BuildIndex(index_dir)
mySql=MySql()
num,cursor=mySql.selectUnIndexCursor()
print 'Total',str(num),'items need to be indexed.'

for row in cursor:
	print 'index id:',row['id']
	print 'index title:',row['title']
	
	bi.addDocuments(str(row['id']),row['title'],row['content'])

cursor.close()
mySql.updateAllIsIndex()

'''
cursor = mySql.selectUpdateCursor()
print '一共有',str(cursor.rowcount()),'条数据需要建立索引'
for row in cursor:
	print 'update id:',row['id']
	print 'update title:',row['title']
	bi.addDocuments(row['id'],row['title'],row['content'])
	bi.updateIsUpdateById(row['id'])
cursor.close()
'''
bi.close()
mySql.close()

