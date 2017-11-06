#coding=utf-8
'''
爬虫
用于抓取网页
并以html文件形式保存至本地

'''

import requests
from bs4 import BeautifulSoup
import re
import codecs

#模拟浏览器登陆的http头
my_headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
}

class Spider:

    stopUrls = [
        "http://blog.csdn.net/error/404.html"
    ]

    #去除无效url的正则表达式
    CLEANURL0 = re.compile(ur'.*html')
    CLEANURL1 = re.compile(ur'')

    #访问过的url表
    visitedUrl = set()

    #存储当前层的链接集合
    linkStack = set()

    #网页文件存储文件夹 暂时需要手动建立
    path = "../pages/"

    #网页文件后缀
    HTMLEXT = ".html"

    #抓取超时等待
    timeOut = 3;

    #当前抓取深度
    currentDepth = 0

    #以 起始url 最大抓取深度 初始化
    def __init__(self, startUrl, maxDepth):
        # 开始抓取的起始URL
        self.startUrl = startUrl
        # 抓取的最大深度
        self.maxDepth = maxDepth
        self.linkStack.add(startUrl)


    #分析页面内所有链接形成栈返回
    def __getPageLink(self, pageText):
        tempStack = set()
        pagesoup = BeautifulSoup(pageText, 'lxml')
        for newUrl in pagesoup.find_all(name='a', attrs={"href": re.compile(r'^http:')}):
            if(newUrl != None):
                urlStr = newUrl.get('href')
                #去除最后的斜线
                if(urlStr[len(urlStr)-1] == '/'):
                    urlStr = urlStr[0:len(urlStr)-1]
                tempStack.add(urlStr)
        #去除无效链接后的结果
        #resStack = set()
        #for url in tempStack:
            #if(re.match(url, self.CLEANURL0)):
                #resStack.add(url)
        #不去重 最后一同去重
        return tempStack

    #保存html文件
    def __saveHtml(self, url, pageText):
        filename = self.path + url.replace('/','_') + self.HTMLEXT
        file = codecs.open(filename, "w", "UTF-8")
        file.write(pageText)
        file.close()

    #访问当前栈内所有链接 并生成新的栈
    def visitCurrent(self):
        if(self.currentDepth >= self.maxDepth):
            print "out of maxdepth"
        else:
            newLinkStack = set()
            count = 1
            for url in self.linkStack:
                try:
                    if( url in self.startUrl):
                        continue
                    if (url in self.visitedUrl):
                        continue
                    else:
                        page = requests.get(url, timeout=self.timeOut, headers=my_headers)
#-------------------------
                        # 只保留成功访问的网页
                        if((page.status_code/100)== 2):
                            print 'ok'
                        else:
                            continue
#-------------------------
                        page.encoding = 'utf-8'
                        newLinkStack |= self.__getPageLink(page.text)
                        # 添加至访问历史，防止重复访问，防止死循环
                        self.__saveHtml(url, page.text)
                        self.visitedUrl.add(url)
                        # 输出完成进度
                except:
                    print 'wrong: ',url,' ',
                finally:
                    print count, "/", len(self.linkStack)
                    count+=1

        self.linkStack = newLinkStack
        self.currentDepth += 1

        return self.currentDepth

'''
print "fetching......"

targetDepth = 2

s = Spider("http://www.baidu.com", targetDepth)


for i in range(1,targetDepth + 1):
    s.visitCurrent()
    print "depth: ",i , '/', s.maxDepth," done"
    
'''
'''
s = re.compile(ur'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')

c = re.compile(ur'https?://')


if(c.match("http://tieba.baidu.com/f?ie=utf8&kw=%E8%B4%B4%E5%90%A7%E6%9B%9D%E5%85%89%E5%8F%B0&fr=wwwt").span()):
    print "ok"
'''

#page = requests.get("http://blog.csdn.net/dev/csdn/article/details/78275444", timeout=3, headers=my_headers)

