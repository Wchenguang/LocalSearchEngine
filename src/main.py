#coding=utf-8

'''
搜索实例
'''

import Engine

engine = Engine.Engine()


'''
for i in engine.targetMap:
    print i, len(engine.targetMap[i]), "条"
    for ii in engine.targetMap[i]:
        if ii[1] > 50:
            print ii[0]
'''
engine.startSearch()