#coding=utf-8

'''
将搜索结果写入 ../result.html
'''

import codecs
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


#html的style
HTMLSTYLE = "\t<style>\n" \
            "\t\tspan {\n" \
            "\t\t\tcolor : red\n" \
           "\t\t}\n" \
            "\t</style>\n" \

class HtmlWriter:

    targetStr = ""

    maxLine = 300

    #获取一个段落的文本
    def __getPara(self, url, brief, startPos, endPos):
        result = "\t\t<p> <a href=\"".encode("utf-8")
        result += url
        result += "\" target=\"view_window\">"
        result += brief[0:startPos]
        result += "<span>"
        result += brief[startPos:endPos + 1]
        result += "</span>"
        result += brief[endPos + 1: len(brief)]
        result += "</a>\n"
        return result

    #构造html
    def write(self, targetList):
        self.targetStr = ""
        index = 0
        for ele in targetList:
            if index >= self.maxLine:
                break
            self.targetStr += self.__getPara(
                ele[0],
                ele[2],
                ele[3],
                ele[4]
            )
            index += 1


