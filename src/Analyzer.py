#coding=utf-8

'''
提供分词接口以及一些工具接口
'''

import jieba

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
    return []