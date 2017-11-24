#coding=utf-8
'''
搜索引擎核心
调用其他模块完成搜索引擎功能
'''

import Spider
import FileAnalyzer
import MapBuilder
import re
import Analyzer
import codecs
import HtmlWriter
import copy

class Engine:

    # 最大关键词长度
    MAXKEYWORDLEN = 16

    #映射表
    targetMap = {}

    #目标url
    targetUrl = "http://www.csdn.net"

    #目标深度
    targetDepth = 2

    #爬虫
    spider = Spider.Spider(targetUrl, targetDepth)

    #文件分析
    htmlIndexer = FileAnalyzer.HtmlIndexer()

    #倒排索引表建立
    mapBuilder = MapBuilder.MapBuilder()

    #匹配摘要前后的文字正则
    #briefPat = ur"[\u4e00-\u9fa5]{"
    #maxBrief = 40
    briefPat = ur"[\u4e00-\u9fa5]{0,40}"

    def __init__(self):
        #抓取
        print "fetching......"
        for i in range(1, self.targetDepth + 1):
            self.spider.visitCurrent()
            print "depth: ", i, '/', self.spider.maxDepth, " done"
        #建立索引文件
        print "indexing......"
        self.htmlIndexer.getHtml()
        self.htmlIndexer.startIndex()
        #获取倒排索引表
        print "mapping"
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

    def __getBrief(self, targetWord, targetResult):
        resList = []
        for res in targetResult:
            try:
                filename = self.spider.path + res[0].replace('/', '_') + self.spider.HTMLEXT
                file = codecs.open(filename, "r", "UTF-8")
                content = file.read()
                '''length = self.maxBrief
                brief = ""
                while(length > 0):
                    brief = re.search(self.briefPat + str(length) + ur'}' + targetWord + self.briefPat + str(length) + ur'}', content)
                    if (brief):
                        break
                    length -= 1'''
                brief = re.search(self.briefPat + targetWord + self.briefPat, content)
                if(brief):
                    string = brief.group()
                    res.append(string)
                    res.append(len(string.split(targetWord)[0]))
                    res.append(res[len(res)-1] + len(targetWord) - 1)
                    resList.append(res)

                file.close()
            except:
                None
        return resList


    def getResult(self, targetWord):

        #截取关键词
        targetWord = targetWord.decode('utf-8')
        if(len(targetWord) > self.MAXKEYWORDLEN):
            targetWord = targetWord[0:self.MAXKEYWORDLEN]

        result = []
        
        #将搜索词作为关键字查找
        #targetWord = targetWord.decode('utf-8')
        #tempResult = self.__getUrlAndWeight(targetWord)
        #tempResult = self.__getBrief(targetWord, tempResult)
        #result += tempResult
        #将分词的结果作为关键字
        #targetSplit = Analyzer.getChiSegList(targetWord, self.htmlIndexer.chiStopWordsList)

        #chiTargetSplit =
        #engTargetSplit =

        targetSplit = Analyzer.getChiSegList(Analyzer.getAllChiInStr(targetWord), self.htmlIndexer.chiStopWordsList) +  Analyzer.getEngSegList(Analyzer.getAllEngInStr(targetWord), self.htmlIndexer.engStopWordsList)

        for word in targetSplit:
            tempResult = self.__getUrlAndWeight(word)
            tempResult = self.__getBrief(word, tempResult)
            result += tempResult
        #将url结果相同的条目合并
        mergedRes = self.__mergeUrlAndWeight(result)
        #将结果按照权重排序
        mergedRes.sort(key=lambda uaw: uaw[1], reverse=True)

        '''for res in mergedRes:
            if(len(res) >= 3):
                mergedRes.remove(res)

        result = []'''

        return mergedRes




    def startSearch(self):
        while(1):
            print "请输入关键字############################################"
            key = raw_input()
            #key = key.decode('utf-8')

            result = self.getResult(key)

            writer = HtmlWriter.HtmlWriter()

            writer.write(result)

            for urlAndWeight in result:
                print urlAndWeight[0], urlAndWeight[1], urlAndWeight[2]


