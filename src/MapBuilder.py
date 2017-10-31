#coding=utf-8
'''
用于读取单词文件
并且建立单词到url的映射
并将map加载至内存
'''

import os
import codecs

class MapBuilder:

    #保存的索引文件的路径
    indexPath = "../indexs/"

    # index文件后缀
    INDEXEXT = ".index"

    #所有.index文件
    allIndexFileNames = []

    #获取所有index文件 其对应链接即文件名
    def __getAllIndexFlies(self):
        list = os.listdir(self.indexPath)
        for name in list:
            path = os.path.join(self.indexPath, name)
            if os.path.isfile(path) and self.INDEXEXT in path:
                self.allIndexFileNames.append(path)

    #将文件名转化为对应url
    def __indexFileName2url(self, indexFileName):
        return indexFileName.split(self.INDEXEXT)[0].split(self.indexPath)[1].replace('_','/')

    #获取倒排索引表
    def getMap(self):
        indexMap = {}
        indexMap[''] = [['',0]]
        self.__getAllIndexFlies()
        for indexFileName in self.allIndexFileNames:
            indexFile = codecs.open(indexFileName, 'r', 'UTF-8')
            #提取url
            url = self.__indexFileName2url(indexFileName)
            while(1):
                word = indexFile.readline()
                if(word == ''):
                    break
                weight = float(indexFile.readline()[0:len(word) - 1])
                #整个单词建立映射
                word = word[0:len(word) - 1]
                #print word
                if (indexMap.has_key(word)):
                    indexMap[word].append([url, weight])
                else:
                    indexMap[word] = []
                    indexMap[word].append([url, weight])
                #每个子建立映射
                '''
                for ch in word:
                    #print ch
                    if (indexMap.has_key(ch)):
                        indexMap[ch].add(url)
                    else:
                        indexMap[ch] = set()
                        indexMap[ch].add(url)
                '''

            indexFile.close()
        return indexMap

'''
m = MapBuilder()

map = m.getMap()

for s in map:
    print s
    for w in map[s]:
        print w
'''