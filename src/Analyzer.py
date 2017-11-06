#coding=utf-8

'''
提供分词接口以及一些工具接口
'''

import re
import jieba
import nltk
from nltk.stem.lancaster import LancasterStemmer

ST = LancasterStemmer()

#合并两个 指向元素为数字的map
def mergeIntMap(self, map1, map2):
    for key1 in map1:
        if(map2.has_key(key1)):
            map1[key1] += map2[key1]
            map2.pop(key1)
    for key2 in map2:
        map1[key2] = map2[key2]
    return map1

#获取中文分词列表
def getChiSegList(sourceStr, stopWordsList):
    resList = []
    segList = jieba.cut(sourceStr)
    for word in segList:
        if (word not in stopWordsList):
            resList.append(word)
    return resList



#获取英文分词列表
def getEngSegList(sourceStr, stopWordsList):
    resList = []
    segList = [word for word in nltk.tokenize.word_tokenize(sourceStr)]
    for word in segList:
        #变为小写 词干化
        word = ST.stem(word.lower())
        if (word not in stopWordsList):
            resList.append(word)
    return resList

#获取字符串所有中文内容
def getAllChiInStr(pageContent):
    words = re.findall(ur"[\u4e00-\u9fa5]+", pageContent)
    str = ""
    if(words != None):
        for word in words:
            str += word
            str += " "
    return str

#获取字符串中所有的英文内容
def getAllEngInStr(content):
    words = re.findall(ur"[a-zA-Z]+", content)
    str = ""
    if (words != None):
        for word in words:
            str += word
            str += " "
    return str

#getEngSegList("fuck Mot MMG nlafg i wanted to fuck your dicks", [])

#getChiSegList("gunas阿斯顿发的时代 你好sd", [])