#coding=utf-8
'''
用于分析html进行分词与索引
建立每个网址url的单词表
并保存至文件
'''

import os
import codecs
import jieba
import jieba.analyse
import re
import collections
from bs4 import BeautifulSoup
import Analyzer

class HtmlIndexer:

    #权重表
    WEIGHT_REALMNAME = 1000
    WEIGHT_TITLE = 100
    WEIGHT_KEYWORDS = 10
    WEIGHT_DISCREPTION = 5
    WEIGHT_WORD = 0.5


    #文本保留最大关键字数
    KEYINTEXTNUM = 30
    # title保留最大关键字数
    KEYINTITLENUM = 3
    # keywords保留最大关键字数
    KEYINKEYWORDS = 5
    # discription保留最大关键字数
    KEYINDISCRIPTION = 7

    #html文件路径
    htmlPath = "../pages/"

    #保存的索引文件的路径
    indexPath = "../indexs/"

    #中文停用词表路径
    chiStopWordsPath = "../ChiStopWords.txt"

    #中文停用词集合
    chiStopWordsList = []

    #英文停用词表路径
    engStopWordsPath = "../EngStopWords.txt"

    #英文停用词表
    engStopWordsList = []

    #网页文件后缀
    HTMLEXT = ".html"

    #index文件后缀
    INDEXEXT = ".index"

    #所有html文件名
    allHtmlFilenames = []

    def __init__(self):
        #加载停用词表
        self.engStopWordsList = [line.strip() for line in codecs.open(self.engStopWordsPath, 'r', 'UTF-8').readlines()]
        self.chiStopWordsList = [line.strip() for line in codecs.open(self.chiStopWordsPath, 'r', 'UTF-8').readlines()]
        self.chiStopWordsList.append(' ')

    #将字符串中的中文逗号换成英文逗号 用于解析
    def __replaceCComa(self, cstr):
        tempstr = u''
        for c in cstr:
            if c == u'，':
                tempstr += ','
            else:
                tempstr += c
        return tempstr

    #合并两个 指向元素为数字的map
    def mergeIntMap(self, map1, map2):
        for key1 in map1:
            if(map2.has_key(key1)):
                map1[key1] += map2[key1]
                map2.pop(key1)
        for key2 in map2:
            map1[key2] = map2[key2]
        return map1


        #将.html文件转化为.index文件
    def __html2index(self, htmlPath):
        path = htmlPath.split(self.HTMLEXT)[0] + self.INDEXEXT
        path = self.indexPath + path.split(self.htmlPath)[1]
        return path

    # 分词接口
    def __getChiSegMap(self, sourceStr, wordNum, weight):
        #tempList = []
        targetMap = {}
        segList = Analyzer.getChiSegList(sourceStr, self.chiStopWordsList)
        #for word in segList:
            #if(word not in self.chiStopWordsList):
                #tempList.append(word)
        tempC = collections.Counter(segList);

        for word,times in tempC.most_common(wordNum):
            targetMap[word] = times * weight

        return targetMap



    def __getEngSegList(self, sourceStr):
        tempList = []
        targetMap = {}
        #英文分词
        segList = jieba.cut(sourceStr)
        for word in segList:
            if (word not in self.engStopWordsList):
                tempList.append(word)
        tempC = collections.Counter(tempList);

        for word, times in tempC.most_common(self.KEYINTEXTNUM):
            targetMap[word] = times * self.WEIGHT_WORD

        return targetMap
    #获取
    def __getKeySeg(self, sourceStr, num, weight):
        keywords = jieba.analyse.extract_tags(sourceStr, topK=num, withWeight=False, allowPOS=('ns', 'n', 'v'))
        targetMap = {}
        for word in keywords:
            targetMap[word] = weight;
        return targetMap

    #获取title内容接口
    def __getHtmlTltle(self, pagesoup):
        if(None != pagesoup.title):
            targetStr = pagesoup.title.string
            if (targetStr != None):
                return targetStr
        return ""

    #获取keywords内容接口
    def __getHtmlKeyWord(self, pagesoup):
        targetStr = ""
        tag = pagesoup.find('meta', attrs={'name': "keywords"})
        if(tag != None):
            sourcestr = tag.get("content")
            if(sourcestr != None):
                if (u'，' in sourcestr):
                    sourcestr = self.__replaceCComa(sourcestr)
                if (',' in sourcestr and u'，' not in sourcestr):
                    for word in sourcestr.split(','):
                        targetStr += word
                        targetStr += ' '
        return targetStr

    #获取discription内容接口
    def __getHtmlDiscription(self, pagesoup):
        targetStr = ""
        tag = pagesoup.find('meta', attrs={'name': "description"})
        if (tag != None):
            tempStr = tag.get("content")
            if(tempStr != None):
                targetStr = tempStr
        return targetStr

    #获取网页所有中文内容
    def __getAllChiInHtml(self, pageContent):
        words = re.findall(ur"[\u4e00-\u9fa5]+", pageContent)
        str = ""
        if(words != None):
            for word in words:
                str += word
                str += " "
        return str

    #为html文件分词
    def __getHtmlIndexs(self, htmlFile):
        pageContent = htmlFile.read()
        pagesoup = BeautifulSoup(pageContent, 'lxml')
        #获取html内关键字及相应权重
        targetMap =  self.__getKeySeg(self.__getHtmlTltle(pagesoup), self.KEYINTITLENUM, self.WEIGHT_TITLE)
        targetMap = self.mergeIntMap(targetMap, self.__getKeySeg(self.__getHtmlKeyWord(pagesoup), self.KEYINKEYWORDS, self.WEIGHT_KEYWORDS))
        targetMap = self.mergeIntMap(targetMap, self.__getKeySeg(self.__getHtmlDiscription(pagesoup), self.KEYINDISCRIPTION, self.WEIGHT_DISCREPTION)
                                     )
        #获取所用中文文本 提取关键字并按照词频赋予权值
        allChi = self.__getAllChiInHtml(pageContent)
        targetMap = self.mergeIntMap(targetMap,self.__getChiSegMap(allChi, self.KEYINTEXTNUM, self.WEIGHT_WORD))

        return targetMap


    #获取所有html文件路径
    def getHtml(self):
        list = os.listdir(self.htmlPath)
        for name in list:
            path = os.path.join(self.htmlPath, name)
            if os.path.isfile(path) and self.HTMLEXT in path:
                self.allHtmlFilenames.append(path)

    #为所有文件分词 每个链接对应的单词表保存为.index文件
    def startIndex(self):
        i = 1
        for htmlFileName in self.allHtmlFilenames:
            #获取所需文件信息
            indexFileName = self.__html2index(htmlFileName)
            htmlFile = codecs.open(htmlFileName, 'r', 'UTF-8')
            indexFile = codecs.open(indexFileName, 'w', 'UTF-8')

            #获取网页的关键字权重表
            indexsAndWeights = self.__getHtmlIndexs(htmlFile)

            #将表写入文件
            for index in indexsAndWeights:
                indexFile.write(index + "\n")
                indexFile.write(str(indexsAndWeights[index]) + "\n")

            htmlFile.close()
            indexFile.close()

            #输出进度
            print i, "/", len(self.allHtmlFilenames)
            i += 1


'''
print "indexing......"
h = HtmlIndexer()
h.getHtml()
h.startIndex()
'''
#h = HtmlIndexer()
#h.startIndex()