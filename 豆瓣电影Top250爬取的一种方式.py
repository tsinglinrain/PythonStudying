from bs4 import BeautifulSoup  #网页解析
import re   #正则表达式
import urllib.request, urllib.error   #指定URL，获取网页数据
import xlwt #进行excel操作
import sqlite3  #进行SQlite数据库操作

def main():
    baseurl = "https://movie.douban.com/top250?start=0"
    #  1.爬取网页
    datalist = getData(baseurl)
    # 3.保存数据
    savepath = "D:\python_study\douban_movie_Top250.xls"
    saveData(datalist, savepath)
    # askURL("https://movie.douban.com/top250?start=0")  测试使用

# 创建全局变量  #创建正则表达式对象，表示规则（—字符串模式）
findlink = re.compile(r'<a href="(.*?)">')    # 影片详情链接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  #让换行符包含在字符中  # 影片图片
findTitle = re.compile(r'<span class="title">(.*)</span>') # 影片片名
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>') #影片评分
findJudge = re.compile(r'<span>(\d*)人评价</span') #找到评价人数
findInq = re.compile(r'<span class="inq">(.*)</span>')  #找到概况
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):     #调用获取页面信息的函数10次数
        url = baseurl +  str(i * 25)
        html = askURL(url)       #保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  #查找符合要求的字符串，形成列表
            # print(item) #测试，查看电影item全部信息
            data = []  #保存一部电影所有信息
            item = str(item)
            
            # 创建影片详情
            link = re.findall(findlink, item)[0]    # re库用于利用正则规则，查找指定字符串
            
            data.append(link)                       # 添加链接
            # print(data)

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(link)                       # 添加图片
            # print(data)

            titles = re.findall(findTitle, item)     # 片名可能只有中文名，没有英文名字
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)         #添加中文名字
                otitle = titles[1].replace("/", "")
                data.append(otitle)         #添加外国名
            else:
                data.append(titles[0])
                data.append(' ')       #外国名留空
            # print(data)

            rating = re.findall(findRating, item)[0]
            data.append(rating)                             #添加评分
            # print(data)

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)                           #添加评价人数
            # print(data)

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "") # 去掉句号
                data.append(inq)            #添加概述
            else:           
                data.append(" ")            #留空
            # print(data)
            
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  #去掉 <br/>
            bd = re.sub('/', " ", bd)   #替换
            data.append(bd.strip())   #去掉空格
            # print(data)    #终于报错了

            datalist.append(data)    #把处理好的一部电影信息放入datalist
    # print(datalist)        
    return datalist


# 得到一个指定URL的网页信息
def askURL(url):
    head = {    # 模拟头部,伪装
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
             AppleWebKit/537.36 (KHTML, like Gecko)\
                 Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

    
# 保存数据
def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet('豆瓣电影Top250')
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i]) #列名称
    
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])  #数据
    
    book.save(savepath)   #保存


if __name__ == "__main__": #当程序执行时
    #调用函数
    main()
    print("爬取完毕！")