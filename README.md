## renrencrawler说明文档

### 技术架构

**Python2.7.10+selenium(2.52.0)+Phantomjs(2.1.1)+BeautifulSoap(4.4.1)**

为什么采用这种方案？

因为人人网许多关键信息都包换在JS脚本里面，所以不能通过使用Python中的liburl这样的库函数来获取数据，可以考虑通过模拟浏览器对也页面进行渲染后得到我们想要挖掘的结果。

* **Selenium**是一个用于Web应用程序测试的工具。Selenium测试直接运行在浏览器中，就像真正的用户在操作一样。支持的浏览器包括IE、Mozilla Firefox、Chrome等。


* **Phantom JS**是一个服务器端的 JavaScript API 的 WebKit。其支持各种Web标准： DOM 处理, CSS 选择器, JSON, Canvas, 和 SVG。

*  **BeautifulSoup**提供一些简单的、python式的函数用来处理导航、搜索、修改分析树等功能。它是一个工具箱，通过解析文档为用户提供需要抓取的数据，因为简单，所以不需要多少代码就可以写出一个完整的应用程序。BeautifulSoup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码。你不需要考虑编码方式，除非文档没有指定一个编码方式，这时，BeautifulSoup就不能自动识别编码方式了。然后，你仅仅需要说明一下原始编码方式就可以了。Beautiful Soup已成为和lxml、html6lib一样出色的python解释器，为用户灵活地提供不同的解析策略或强劲的速度。

  *这里面引用的是官方解释*

  本程序采用的是`lxml HTML 解析器`，优点是速度快，文档容错能力强，需要提前安装。

Selenium注重对单个元素的操作，BeautifulSoup注重对html页面的分析和数据分类处理，所以两者结合可以达到非常好的效果

XPath 是一种在 XML 文档中定位元素的语言。因为 HTML 可以看做 XML 的一种实现，所以 selenium 用户可是使用这种强大语言在 web 应用中定位元素。



### 参考资料

[BeautifulSoap4.2.0中文文档](http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/index.html)

[Python爬虫之BeautifulSoap的用法](http://cuiqingcai.com/1319.html)

[selenium python 官方文档](https://selenium.googlecode.com/svn/trunk/docs/api/py/index.html)

[PhantomJS使用说明](http://www.tuicool.com/articles/nieEVv)