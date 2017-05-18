import lucene
from lucene import ChineseAnalyzer,IndexWriter,SimpleFSDirectory,Field,File,Document

class BuildIndex:
	def __init__(self,indir):
		lucene.initVM()
		indexdir=SimpleFSDirectory(File(indir))
		self.index_writer= IndexWriter(indexdir,self.getAnalyzer(),True,IndexWriter.MaxFieldLength(512))
	def getAnalyzer(self):
		return ChineseAnalyzer(lucene.Version.LUCENE_CURRENT)
	def addDocuments(self,_id,title,content):
		doc = Document()
		doc.add(Field("id", _id,Field.Store.YES,Field.Index.NOT_ANALYZED))
		if title is not None and len(title)>0:
			doc.add(Field("titleKeyword",title,Field.Store.NO,Field.Index.ANALYZED))
		if content is not None and len(content)>0:
			doc.add(Field("contentKeyword",content,Field.Store.NO,Field.Index.ANALYZED))
		self.index_writer.addDocument(doc)
	def close(self):
		self.index_writer.optimize()
		self.index_writer.close()