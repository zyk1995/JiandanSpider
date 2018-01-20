__author__="ZYK"
# -*- coding:utf-8 -*-
import requests
from proxy import Proxy
from bs4 import BeautifulSoup
# 导入selenium模块中的web引擎
from selenium import webdriver

import re
import tool
import ssl
import os
import sys

proxy = Proxy()
#-----------------------------------
#煎蛋网爬虫
#-----------------------------------
class Spider:

    def __init__(self,url):
        self.siteURL =  url
        self.headers = {
        	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) '
        	             +'AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
            'Accept'	: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer'   : 'https://jandan.net/ooxx',
            'Upgrade-Insecure-Requests':	'1'}
        # 建立浏览器对象 ，通过Phantomjs
        self.browser = webdriver.PhantomJS()

    #--------------------------------
    #通用方法
    #封装常用到的代码减少代码量
    #openUrl(url)
    #mkdir(path)
    #writeToFile(path,name,data)
    #--------------------------------

    #访问网络资源
    def openUrl(self, url):

        # 访问url
        self.browser.get(url)

        # 等待一定时间，让js脚本加载完毕
        self.browser.implicitly_wait(3)

        print(self.browser.title)
        picList = []
        picUrlList = self.browser.find_elements_by_css_selector("a.view_img_link")

        for picUrl in picUrlList:
            picUrl = picUrl.get_attribute("href")
            print(picUrl)
            picList.append(picUrl)



        return picList
    #创建文件夹
    def mkdir(self, path):
        path = path.strip()

        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print ("创建目录"+path)
            return True
        else:
            print (u'名为'+path+'的文件夹已经存在')
            return False
    #保存数据到本地
    def writeToFile(self, path, name, data):
        f = open(path + "/" + name,'wb')
        f.write(data)
        print ("数据" + name + "已保存到本地" + path)
        f.close()

    #----------------------------------
    #Spider方法
    #
    #----------------------------------
    def getPagePics(self, pageIndex):
        url = self.siteURL + "/page-"+str(pageIndex)
        print ("正在爬取页面" + url)
        pics = self.openUrl(url)
        return pics

    def downloadFile(self, items, target_path):
        self.mkdir(target_path)
        print("正在下载文件...")
        for i, item in enumerate(items):
            print ("正在下载文件（ %d ）%s " % (i, item))
            image_name= str(i)+item[-4:]
            resp = self.openUrl(item)
            self.writeToFile(target_path, image_name, resp.text)
    def downloadImage(self, items, target_path="./Photo"):
           self.mkdir(target_path)
           print("正在下载图片...")

           for i, item in enumerate(items):
                print ("正在下载图片（ %d ）%s " % (i, item))
                image_name= str(i)+item[-4:]
                resp = self.openUrl("http:" + item)
                self.writeToFile(target_path, image_name, resp.text)
    #----------------------------------
    #爬虫方法
    #实现分步爬虫，降低耦合性
    #----------------------------------
    def crawlPage(self, index):
        print ("正在爬取第" + str(index) + "页")
        pics = self.getPagePics(index)
        self.downloadImage(pics, "./meizitu" + str(index))
    #----------------------------------------
    #批量爬取页面
    #----------------------------------------
    def crawl(self, start, end):

        for i in range(start, end):
            self.crawlPage(i)
            print ("开始爬取下一个页面")

        # 关闭浏览器
        self.browser.quit()
if __name__ == '__main__':

    '''
    #传入命令行参数
    if(len(sys.argv) != 3):
        print("正确的使用方法：输入一个起始页码，一个终止页码！")
        exit()

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    if(start > end) :
        print("起始页码不能大于终止页码")
        exit()
    '''
    url = 'https://jandan.net/ooxx'
    spider = Spider(url)
    spider.crawl(1, 500)




