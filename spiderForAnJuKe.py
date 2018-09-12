import requests
from bs4 import BeautifulSoup
import math
import time
import random
import regex
from openpyxl import load_workbook
from fake_useragent import UserAgent

class spiderForAnJuKe:
    def __init__(self,city,regionOne):
        self.city = city
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'https: // nb.anjuke.com / sale /?from=navigation',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.regionOne =regionOne
    def getErShouFangArea(self):
        print("开始加载excel")
        self.wb = load_workbook("./doc/data3.xlsx")
        self.write_sheet = self.wb['Sheet1']
        link_one = "https://"+self.city+".anjuke.com/community/"
        response = requests.get(link_one,headers =self.headers)
        soup_one = BeautifulSoup(response.text,"lxml")
        aList = soup_one.select("body > div.w1180 > div.div-border.items-list > div:nth-of-type(1) > span.elems-l > a")
        self.aLinkList = []
        for i in range(1,len(aList)):
            self.aLinkList.append(aList[i]["href"])
        print(self.aLinkList)
    def alterUserAgent(self):
        ua = UserAgent()
        print(ua.random)
        self.headers["User-Agent"] = ua.random
    def getErShouFang(self):
        for link_two in self.aLinkList:
            ip = ['121.31.159.197', '175.30.238.78', '124.202.247.110']
            self.headers["X-Forwarded-For"] = ip[random.randint(0, 2)]

            response_two = requests.get(link_two,headers = self.headers)
            # time.sleep(5)
            soup_two =  BeautifulSoup(response_two.text,"lxml")
            numOfPage = math.ceil(float(soup_two.select("#list-content > div.sortby > span > em:nth-of-type(2)")[0].text)/30)
            print(numOfPage)
            for index in range(1,numOfPage+1):
                link_three = link_two + "p" +str(index)
                response_three = requests.get(link_three,headers = self.headers)
                self.alterUserAgent()
                # time.sleep(5)
                count = 0
                while count <5:
                    try:
                        soup_three = BeautifulSoup(response_three.text,"lxml")
                        ua = UserAgent()
                        liList= soup_three.select("#list-content > div.li-itemmod")
                        for li in liList:
                            a = li.find("a")
                            title = a["title"]
                            address = li.find("address").text.strip()
                            regionTwo = None
                            regionThree = None
                            if regex.search(r'(?<=\［)\w*(?=-)',address):
                                regionTwo = regex.search(r'(?<=\［)\w*(?=-)',address).group()
                            if regex.search(r'(?<=-)\w*(?=\］)',address):
                                regionThree = regex.search(r'(?<=-)\w*(?=\］)',address).group()
                            date = li.select('p.date')[0].text.strip()

                            if regex.search(r'(?<=：\s*)\d*(?=年)',date):
                                buildYear= regex.search(r'(?<=：\s*)\d*(?=年)',date).group()
                            typeOfHouse = None
                            price = li.select('div.li-side > p:nth-of-type(1) > strong')[0].text.strip()
                            others = False
                            regionOne = self.regionOne
                            row = [regionOne,regionTwo,regionThree,others,title,typeOfHouse,buildYear,price]
                            print(row)
                            self.write_sheet.append(row)
                    except Exception as e:
                        count = count+1
                        if count == 5:
                            with open('./doc/error/error.txt',"a+",encoding="utf-8") as ferr:
                                ferr.write("出错的链接是"+link_three+"，错误的原因是"+str(e)+"\n")
                            with open('./doc/error/errLink.txt',"a+",encoding="utf-8") as ferrLink:
                                ferrLink.write(link_three+"\n")
                    else:
                        break
            # print("正在保存")
            # self.wb.save("./doc/data.xlsx")
