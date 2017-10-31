#coding=utf-8
'''
搜索引擎核心
调用其他模块完成搜索引擎功能
'''

import Spider
import FileAnalyzer
import MapBuilder
import copy
import Analyzer

class Engine:

    #映射表
    targetMap = {}

    #目标url
    targetUrl = "http://www.csdn.net"

    #目标深度
    targetDepth = 3

    #爬虫
    spider = Spider.Spider(targetUrl, targetDepth)

    #文件分析
    htmlIndexer = FileAnalyzer.HtmlIndexer()

    #倒排索引表建立
    mapBuilder = MapBuilder.MapBuilder()

    def __init__(self):
        #抓取
        #for i in range(1, self.targetDepth + 1):
         #   self.spider.visitCurrent()
          #  print "depth: ", i, '/', self.spider.maxDepth, " done"
        #建立索引文件
        print "indexing......"
        #self.htmlIndexer.getHtml()
        #self.htmlIndexer.startIndex()
        #获取倒排索引表
        self.targetMap = self.mapBuilder.getMap()

    def __getUrlAndWeight(self, word):
        res = []
        if (word in self.targetMap):
            res = self.targetMap[word]
        return res

    def __mergeUrlAndWeight(self, result):
        ans = []
        while 0 != len(result):
            temp = result[0]
            result.remove(temp)
            i = 0
            while i >= 0 and i < len(result):
                if (result[i][0] == temp[0]):
                    temp[1] += result[i][1]
                    result.remove(result[i])
                    i = i - 1
                i = i + 1
            ans.append(temp)
        return ans

    def __getResult(self, targetWord):
        result = []
        
        #将搜索词作为关键字查找
        targetWord = targetWord.decode('utf-8')
        result += self.__getUrlAndWeight(targetWord)
        #将分词的结果所谓关键字
        targetSplit = Analyzer.getChiSegList(targetWord, self.htmlIndexer.chiStopWordsList)
        for word in targetSplit:
            result += self.__getUrlAndWeight(word)
        #将url结果相同的条目合并
        mergedRes = self.__mergeUrlAndWeight(result)
        #将结果按照权重排序
        mergedRes.sort(key=lambda uaw: uaw[1], reverse=True)

        return mergedRes




    def startSearch(self):
        while(1):
            print "请输入关键字############################################"
            key = raw_input()
            #key = key.decode('utf-8')

            result = self.__getResult(key)
            for urlAndWeight in result:
                print urlAndWeight[0], urlAndWeight[1]


