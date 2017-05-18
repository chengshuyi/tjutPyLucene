# -*- coding: utf-8 -*-
import scrapy

from tjutScrapy.MySql import MySql
from tjutScrapy.items import TjutscrapyItem
import time
from bs4 import BeautifulSoup
from urlparse import urljoin

class TjutSpider(scrapy.Spider):
    name = "tjut"
    allowed_domains = ["tjut.edu.cn"]
    start_urls = []

    idList=[['id','vsb_newscontent'],['class','zw_content'],['id','vsb_content']]

    incTime=86400

    maxId=0

    hashUrl={}

    def __init__(self):
        self.mysql=MySql()
        self.hashUrl=self.mysql.buildHashForUrl()

        curTime=int(time.time())
    
        for item in self.hashUrl:
            #超过下一次的规定时间，加入队列
            if self.hashUrl[item][self.mysql.next_scrawl_time]<=curTime:
                self.start_urls.append(item)

        self.maxId=self.mysql.getMaxId()

        if len(self.start_urls)==0:
            self.start_urls.append('http://www.tjut.edu.cn/')

    def parse(self, response):

        update=False
        new_url=False
        url=''
        title=''
        keyword=''
        content=''
        last_modified=0
        pre_last_modified=0
        _id = 0
        next_scrawl_time=0

        a_tag=[]
        
        soup=BeautifulSoup(response.text,'html.parser')
        url=response.url
        try:
            title=soup.title.string
        except Exception,e:
            print Exception,":",e
        try:
            keyword = soup.find(attrs={'name':'keywords'})['content']
        except Exception,e:
            print Exception,":",e
        
        for item in self.idList:
            try:
                content = soup.find(attrs={item[0]:item[1]}).text
            except Exception,e:
                print Exception,":",e
                continue
            break
            
        try:
            last_modified=timeToTimeStamp(response.headers['Last-Modified'])
        except Exception,e:
            last_modified=int(time.time())
            print Exception,":",e
        
        try:
            a_tag = soup.find_all('a')
        except Exception,e:
            print Exception,":",e

        if url in self.hashUrl:
            pre_last_modified=self.hashUrl[url][self.mysql.last_modified]
            if pre_last_modified < last_modified:
                update=True
                next_scrawl_time=2*last_modified-pre_last_modified
            _id = self.hashUrl[url][self.mysql._id]
        else:
            new_url=True
            self.maxId+=1
            _id=self.maxId
            next_scrawl_time=last_modified+self.incTime
            self.hashUrl[url]={
                self.mysql._id:self.maxId,
                self.mysql.last_modified:last_modified,
                self.mysql.next_scrawl_time:next_scrawl_time
            }
        
        yield TjutscrapyItem({'update':update,'next_scrawl_time':next_scrawl_time,'_id':_id,'new_url':new_url,'url':url,'title':title,'keyword':keyword,'content':content,'last_modified':last_modified})
        #print 'a_tag:',a_tag
        for link in a_tag:
            url = urljoin(response.url, link.get('href'))
            if url not in self.hashUrl:
                #自己去重
                yield scrapy.Request(, callback=self.parse)


def timeToTimeStamp(time_str):
    timeArray = time.strptime(time_str, "%a, %d %B %Y %H:%M:%S %Z")
    return int(time.mktime(timeArray))
