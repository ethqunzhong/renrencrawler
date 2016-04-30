# -*- coding: utf-8 -*-
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys  # 引入Keys类操作
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.action_chains import ActionChains  # 引入ActionChains鼠标操作类
# from selenium.webdriver.common.keys import Keys
import sys
import urllib2
import time
from bs4 import BeautifulSoup
import urllib
import os
import re


# *************************************************************
def ProducePath(Input_Path):  # 生成文件存储目录
    try:
        Input_Path = Input_Path.encode('utf-8')  # 以 utf-8 编码
        Input_Path = Input_Path.decode('utf-8').encode('gbk', 'ignore')  # 解码成中文，忽略错误

        if os.path.isdir(Input_Path):
            pass
        else:
            os.makedirs(Input_Path)
    except:
        print u'生成文件夹错误'
    return Input_Path


def WriteData(Data, FilePath):  # 将爬到数据写入指定filepath
    try:
        if FilePath is not None:
            f = open(FilePath, "wb")  # 二进制写入
            f.write(Data)
            f.flush()
            print FilePath
            f.close()
    except:
        print u'写入文件错误'


def FriendInfo(Ruid_info):
    try:
        Info_Flag = 0
        while Info_Flag == 0:
            print u'请输入好友ID，好友ID可以通过浏览器访问好友主页来查看，地址栏上面的一串数字'
            Friend_ID_info = raw_input(u"Friend_ID:   ")
            # Friend_ID_info=raw_input(u"请输入好友ID号(地址栏上8位数字): ")
            currentUrl = "http://www.renren.com/" + Friend_ID_info + "/profile?portal=homeFootprint&ref=home_footprint"
            driver.get(currentUrl)
            time.sleep(2)

            TempSource = driver.page_source  # 获取当前页面资源
            pattern = re.compile(r'ruid:.*?"(\d+)"', re.S)  # 编译正则表达式，. 包含匹配换行符

            Ruid_Friend = re.findall(pattern, TempSource)  # 返回所有匹配子串（list）  不要搞错了
            if Ruid_Friend == Ruid_Self:
                Info_Flag = 1
                print u'获取好友信息成功'

            else:
                print u'获取好友信息失败，请重新输入好友ID'
        return Friend_ID_info
    except:
        print u'好友输入失败'


# ***************************************************************************
try:
    SleepTimeCount1 = 2
    driver = webdriver.PhantomJS()  # webdriver 支持PhantomJS伪浏览器驱动  不用打开浏览器了
    # executable_path="C:\phantomjs-2.1.1-windows\phantomjs.exe"
    print u'欢迎使用本工具下载人人照片，日志，状态'
    print

    LoginFlag = 0
    # 设置一个 BreakFlag 用来中途按键退出
    # ****************************模拟登陆操作******************************
    while LoginFlag == 0:
        driver.get("http://www.renren.com")
        LoginName = raw_input(u"please input the user email: ")
        LoginPassword = raw_input(u"input the password: ")
        # 控件属性例如id、name、等等 xpath语言参考文档
        driver.find_element_by_xpath('//input[@name="email"]').send_keys(LoginName)
        driver.find_element_by_xpath('//input[@name="password"]').send_keys(LoginPassword)
        # driver.get_screenshot_as_file('show.png')
        # xpath 参考资料
        driver.find_element_by_xpath('//form[@id="loginForm"]').submit()  # 提交表单，登陆
        time.sleep(2)
        TempSource = driver.page_source
        soup = BeautifulSoup(TempSource, "lxml")  # 调用 lxml HTML 解析器
        pattern = re.compile(r'ruid:.*?"(\d+)"', re.S)
        Ruid_Self = re.findall(pattern, TempSource)
        if len(Ruid_Self[0]) > 4:  # 识别当前用户id 一般是9位数字，所以这里可以用来作为判断条件
            print u'登陆成功'
            Main_url = driver.current_url  # 获取当前页面的所有URL
            index1 = Main_url.find(r'renren.com/')
            User_ID = Main_url[index1 + 11:100]  # renren.com/ 以后的部分作为User_ID
            AccountName = soup.title.contents[0]  # <title>人人网 - XXX</title><meta charset="utf-8"/>
            # print AccountName
            AccountName = AccountName[6:]  # XXX
            print u'登陆ID:' + User_ID + '     ' + u'用户名:' + AccountName
            print
            time.sleep(2)
            LoginFlag = 1
        else:
            LoginFlag = 0
            print u'登陆失败，请重新输入'

    # *****************************选择用户进行下载**********************************
    DownloadFlag = 0
    while DownloadFlag == 0:
        # UserFlag=raw_input(u"1_self, 2_friend")
        print u'请选择：1下载自己信息，2下载朋友信息'
        UserFlag = raw_input(u"1_self, 2_friend: ")
        # UserFlag=raw_input(u"请输入数字，1代表下载自己信息，2代表下载好友信息:	")
        if UserFlag == '1':
            FriendFlag = 0
            SelfFlag = 1
            DownloadFlag = 1
        elif UserFlag == '2':
            SelfFlag = 0
            Friend_ID = FriendInfo(Ruid_Self)  # 输入用户ID
            TempSource = driver.page_source
            soup = BeautifulSoup(TempSource, "lxml")
            FriendName = soup.title.contents[0]
            FriendName = FriendName[6:]
            print u'好友ID:' + Friend_ID + '     ' + u'好友名:' + FriendName

            FriendName = re.sub(r'(\\)|(\/)|(\?)|(\<)|(\>)|(\.)|(\:)|(\*)|(\")|(\|)', '_', FriendName)
            # 去掉标题不兼容关键字

            FriendFlag = 1
            DownloadFlag = 1
        else:
            FriendFlag = 0
            SelfFlag = 0
            print u'输入错误'

    while DownloadFlag:
        # download info
        # download Photo
        print
        print u'开始下载照片'
        if FriendFlag:  # Friend
            currentUrl = "http://photo.renren.com/photo/" + Friend_ID + "/albumlist/v7?showAll=1#"
        else:  # User
            currentUrl = "http://photo.renren.com/photo/" + User_ID + "/albumlist/v7?showAll=1#"
        driver.get(currentUrl)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "lxml")
        PhotoInfo = soup.find_all('div', class_="album-info")  # 抓取所有相册
        # 搜索当前tag的所有子节点，并判断是否符合过滤器的条件
        # 查找所有名字为 div 的tag ，通过 class_ 参数来搜索指定CSS类名的tag
        # 搜索相册标签
        for each in PhotoInfo:  # 对每个相册里面的照片进行下载
            if each != None:
                title = each.contents[1]['title']
                if FriendFlag:
                    current_path = './' + FriendName + u'/照片/' + title
                else:
                    current_path = './' + AccountName + u'/照片/' + title
                current_path = ProducePath(current_path)  # 以该路径名生成相应的文件夹

                globalCount = 0

                link = each.contents[1]['href']
                PhotoUrl = link
                driver.get(PhotoUrl)
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, "lxml")

                allImg = soup.find_all('div', class_="photo-box")  # 找出当前相册所有照片
                for each1 in allImg:
                    imgUrl = each1.contents[1].contents[1]['data-viewer']  # .contents[]
                    index1 = imgUrl.find(r'url')  # 返回url的索引index
                    index2 = imgUrl.find(r'.jpg')
                    Detail_Photo_Url = imgUrl[index1 + 6:index2 + 4]  # 图片所在的具体URL
                    # print Detail_Photo_Url
                    imgPath = current_path + '/' + str(globalCount + 1) + '.jpg'
                    urllib.urlretrieve(Detail_Photo_Url, imgPath)
                    print imgPath
                    globalCount += 1

                    #  ******************************下载日志**********************************
        print
        print u'开始下载日志'
        if FriendFlag:
            current_path = './' + FriendName + u'/日志'  ####
        else:
            current_path = './' + AccountName + u'/日志'  ####
        current_path = ProducePath(current_path)

        if FriendFlag:
            currentUrl = "http://blog.renren.com/blog/" + User_ID + "/blogs/" + Friend_ID
        else:
            currentUrl = "http://blog.renren.com/blog/" + User_ID + "/myBlogs"
        driver.get(currentUrl)
        time.sleep(2)

        TempSource = driver.page_source
        pattern = re.compile(r'<a.*?page-item.*?/a>', re.S)
        NumofPage = re.findall(pattern, TempSource)
        if len(NumofPage) > 2:
            PageFlag = 1
        else:
            PageFlag = 0

        globalCount = 0
        Rizhi_Url = []

        while PageFlag:
            pattern = re.compile(r'<h3.*?blogList-info-title.*?href="(.*?)".*?/h3>', re.S)
            DiaryContents = re.findall(pattern, TempSource)
            for each1 in DiaryContents:
                Rizhi_Url.append(each1)

            pattern = re.compile(r'blogList_myblogPage.*?page-current.*?page-item(.*?)page-next.*?page-disable.*?/a>',
                                 re.S)
            NextPage = re.findall(pattern, TempSource)

            if len(NextPage) > 0:  # 不能再翻页了
                PageFlag = 0
            else:  # 翻页
                globalCount += 1
                Temp_str1 = "//div[@id='blogList_myblogPage']/a[" + str(len(NumofPage)) + "]"
                driver.find_element_by_xpath(Temp_str1).click()
                time.sleep(2)
                TempSource = driver.page_source
        for each1 in Rizhi_Url:
            Detail_Rizhi_Url = each1
            driver.get(Detail_Rizhi_Url)
            time.sleep(2)
            Tempstr = driver.page_source
            Tempstr = re.sub(r'<iframe.*?id="webpagerengine".*?</iframe>', '', Tempstr)
            Tempstr = re.sub(r'<script.*?s.xnimg.cn/a73643/.*?</script>', '', Tempstr)
            soup = BeautifulSoup(Tempstr, "lxml")
            RizhiTitle = soup.h2.contents[0]
            RizhiTitle = re.sub(r'(\\)|(\/)|(\?)|(\<)|(\>)|(\.)|(\:)|(\*)|(\")|(\|)', '_', RizhiTitle)  # 去掉标题不兼容关键字

            if FriendFlag:
                RizhiPath = './' + FriendName + u'/日志' + '/' + RizhiTitle + '.html'
            else:
                RizhiPath = './' + AccountName + u'/日志' + '/' + RizhiTitle + '.html'
            RizhiPath = RizhiPath.encode('utf-8')
            RizhiPath = RizhiPath.decode('utf-8').encode('gbk', 'ignore')

            data = soup.encode('UTF-8')
            WriteData(data, RizhiPath)

        # **************************download status***************************************
        print
        print u'开始下载状态'
        if FriendFlag:
            current_path = './' + FriendName + u'/状态'
        else:
            current_path = './' + AccountName + u'/状态'
        current_path = ProducePath(current_path)

        if FriendFlag:
            currentUrl = "http://status.renren.com/status/v7/" + Friend_ID
        else:
            currentUrl = "http://status.renren.com/status/v7/" + User_ID
        driver.get(currentUrl)
        time.sleep(2)

        TempSource = driver.page_source
        pattern = re.compile(r'<a.*?page-item.*?/a>', re.S)
        NumofPage = re.findall(pattern, TempSource)
        if len(NumofPage) > 2:  # 至少有两个<a ... page-item .../a> 上一页 和 下一页
            PageFlag = 1
        else:
            PageFlag = 0

        globalCount = 1
        while PageFlag:
            StatusPath = current_path + '/page' + str(globalCount) + '.html'
            globalCount += 1
            TempSource = re.sub(r'<iframe.*?id="webpagerengine".*?</iframe>', '', TempSource)  # 替换无用信息
            data = TempSource.encode('UTF-8')

            WriteData(data, StatusPath)

            pattern = re.compile(r'<a.*?page-next.*?page-disable.*?/a>', re.S)  #最后一页的标志 page-disable
            NextPage = re.findall(pattern, TempSource)
            if len(NextPage) > 0:  # 到最后一页了。不能翻页了
                PageFlag = 0
            else:  # 翻页
                # id为 my-status-page 的 div,定位里面的<a></a> , a[NumofPage] 指向的是<a>下一页</a> 这个按钮的位置
                Temp_str = "//div[@id='my-status-page']/a[" + str(len(NumofPage)) + "]"
                driver.find_element_by_xpath(Temp_str).click()
                time.sleep(2)
                TempSource = driver.page_source

        # download complete
        print
        print u'相册，日志，状态下载完成'
        print
        if SelfFlag == 1:
            SelfFlag = 0

        driver.get(Main_url)
        print u'请选择：1继续下载，2退出'
        ContinueFlag = raw_input(u"1_continue,2_exit: ")
        if ContinueFlag == '1':
            Friend_ID = FriendInfo(Ruid_Self)  # 输入用户ID
            TempSource = driver.page_source
            soup = BeautifulSoup(TempSource, "lxml")
            FriendName = soup.title.contents[0]
            FriendName = FriendName[6:]
            FriendName = re.sub(r'(\\)|(\/)|(\?)|(\<)|(\>)|(\.)|(\:)|(\*)|(\")|(\|)', '_', FriendName)  # 去掉标题不兼容关键字
            print u'好友ID:' + Friend_ID + '     ' + u'好友名:' + FriendName
            FriendFlag = 1
            DownloadFlag = 1
        else:
            FriendFlag = 0
            DownloadFlag = 0
    driver.quit()

except:
    print u'程序错误,退出'
    driver.quit()
