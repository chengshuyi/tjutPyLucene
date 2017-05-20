from django.http import HttpResponse
from django.shortcuts import render
import lucene
import pymysql.cursors

from lucene import getVMEnv,SimpleFragmenter,SimpleHTMLFormatter,QueryScorer,StringReader,QueryParser, IndexSearcher, ChineseAnalyzer, SimpleFSDirectory, File, VERSION, initVM, Version,Highlighter
#import jieba

initVM()
STORE_DIR='.././data/index'
directory = SimpleFSDirectory(File(STORE_DIR))
searcher = IndexSearcher(directory, True)
analyzer = ChineseAnalyzer(Version.LUCENE_CURRENT)

db_name='test'
user='root'
password='123456'

def index(request):
    return render(request,'tjut/index.html')


def search(request):

    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    
    ret={}
    maxLength=38

    search_content=request.GET.get('content')
    if len(search_content)>maxLength:
        pass

    query = QueryParser(Version.LUCENE_CURRENT, "contentKeyword",analyzer).parse(search_content)
    scoreDocs = searcher.search(query, 50).scoreDocs

    scorer = QueryScorer(query)
    formatter = SimpleHTMLFormatter("<span class=\"highlight\">", "</span>")
    highlighter = Highlighter(formatter,scorer)
    fragmenter = SimpleFragmenter(50)
    highlighter.setTextFragmenter(fragmenter)

    ret['NumOfDocs']=str(len(scoreDocs))+"total matching documents." 

    print ret['NumOfDocs']

    
    conn=pymysql.connect(   host='localhost',
                            user=user,
                            password=password,
                            db=db_name,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    rst=''
    ret['search_list']=[]
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        _id=str(doc.get("id"))
        print _id
        sql='select * from webpage where id=%s'

        with conn.cursor() as cursor:
            cursor.execute(sql,(_id))
            rst=cursor.fetchone()
                
        titleStream = ChineseAnalyzer(Version.LUCENE_CURRENT).tokenStream("title", StringReader(rst['title']))
        titleFragment = highlighter.getBestFragment(titleStream, rst['title'])
        if titleFragment is None:
            titleFragment=rst['title']

        contentStream = ChineseAnalyzer(Version.LUCENE_CURRENT).tokenStream("content", StringReader(rst['content']))
        contentFragment = highlighter.getBestFragments(contentStream, rst['content'],5,'...')

        ret['search_list'].append({'title':titleFragment,'url':rst['url'],'content':contentFragment})
    #searcher.close()
    conn.close()

    return render(request,'tjut/result.html',{'search_list':ret['search_list'],'search_content':search_content})
