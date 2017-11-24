单机搜索引擎模型
====
<br/>
##使用示例
* 输入目的网址<br/>
<pre>
	/* 修改/src/Engine.py 中25行的目的url 默认是csdn */ <br/>
	#目标url
    targetUrl = "http://www.csdn.net"
</pre> <br/>
* 运行 /src/Exchanger.py 脚本，进行网页抓取与索引的建立并开启本地web服务 

* 打开 /search.htm，输入关键词即可搜索 <br/>  <br/>
![use example](https://github.com/Wchenguang/LocalSearchEngine/blob/master/使用样例.png) <br/>

##实现简介
* /src/Spider.py
	* 网络爬虫
	* 利用BFS(深度优先搜索)，可以设置搜索根url，也可以设置搜索的深度
* /src/FileAnalyzer.py /src/MapBuilder.py
	* 分析抓取的html文件进行倒排索引的建立
	* 倒排索引：即 关键词对应url列表的映射
* /src/Engine.py
	* 利用以上三者，构建搜索引擎核心功能，并提供搜索接口
* ／src/Exchanger.py
	* 实现兼容WebSocket，与前端 result.htm 利用本机回环进行通信 