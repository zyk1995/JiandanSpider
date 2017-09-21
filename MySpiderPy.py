__author__="ZYK"
# -*- coding:utf-8 -*-
import urllib
from urllib import request
import re
import tool
import ssl
import os

class Spider:

    def __init__(self,url):
        self.siteURL =  url
        self.headers = {
        	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) '
        	             +'AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
            'Accept'	: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer'   : 'https://jandan.net/ooxx',
            'Upgrade-Insecure-Requests':	'1'

        }


    def getPage(self, pageIndex):
        url = self.siteURL + "/page-"+str(pageIndex)+'#comments'
        print ("正在爬取页面" + url)
        req = request.Request(url, headers=self.headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = request.urlopen(req,context=gcontext)
        page = response.read().decode('utf-8')
        #print (page)
        return page

    def downloadImage(self, items):
           direct_path='/Users/zhangyikun/Documents/Photo'
           print("正在下载图片...")

           for i, item in enumerate(items):
                print ("正在下载图片（ %d ）%s " % (i, item))
                image_path= direct_path+"煎蛋网妹子图片"+str(i)+".jpg"
                f=open(image_path,'wb')
                f.write(item)
                f.close()
    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        #pattern = re.compile('/large/((.+)\.jpg)""',re.S)

        pattern = re.compile('<img src="(//wx4.sinaimg.cn/.*?)"',re.S)
        print ("正在匹配...")
        items = re.findall(pattern,page)

        for i, item in enumerate(items):
            print ("匹配到的内容（ %d ）%s " % (i, item))

        self.downloadImage(items)


    def mkdir(self, path):
    	path = path.strip();

    	isExists=os.path.exists(path)
    	if not isExists:
    		os.makedirs(path)
    		print ("创建目录"+path)
    		return True
    	else:
    		print (u'名为'+path+'的文件夹已经存在')
    		return False
url = 'https://jandan.net/ooxx'
spider = Spider(url)
#spider.getPage(100);
spider.getContents(100)
