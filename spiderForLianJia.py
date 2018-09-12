import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import time
class spiderForLianJia:
    '''
    initialize class,get the value of cityList, and set value for linkDict and cityDict
    Args:
        cityList: the list of cities we intend to crawl from Lianjia, set the default value be empty
    '''
    def __init__(self,cityList,cityDict):
        self.cityList = cityList
        self.linkDict = {}
        self.cityDict= cityDict
    '''
    get links of all the regions(in detail),both save the results in the linkDict(the attr of the class) and files in the ./doc/link named after the city

    '''
    def getLinks(self):
        cityList =self.cityList

        for city in cityList:
            linkList = []
            link_all = "https://"+city+".lianjia.com"
            link_one = "https://"+city+".lianjia.com/xiaoqu/"
            response_one = requests.get(link_one,verify=False)
            soup_one = BeautifulSoup(response_one.text,"lxml")
            divErShouFang = soup_one.find_all("div",attrs={"data-role":"ershoufang"})[0]#根据html5元素分析页面
            regionTwoListLinks = divErShouFang.find_all("a")
            for regionTwoLink in regionTwoListLinks:
                remotePlace = False
                if regionTwoLink["href"].startswith("https"):
                    link_two = regionTwoLink["href"]
                else:
                    link_two = link_all + regionTwoLink["href"]
                if not link_two.startswith("https//"+city):
                    remotePlace = True
                response_two =requests.get(link_two,verify=False)
                soup_two = BeautifulSoup(response_two.text,"lxml")
                divErShouFang2 = soup_two.find_all("div",attrs={"data-role":"ershoufang"})[0].find_all("div")[1]

                regionThreeListLinks = divErShouFang2.find_all("a")
                for regionThreeLink in regionThreeListLinks:
                    if remotePlace:
                        link_three = "https://"+link_two.split("/")[2]+regionThreeLink["href"]
                    else:
                        link_three = link_all + regionThreeLink["href"]
                    if not  link_three in linkList:
                        linkList.append(link_three)
                        with open("./doc/link/"+city+".txt","a+",encoding="utf-8") as f:
                            f.write(link_three+"\n")
            self.linkDict[city] = linkList
    '''
        judge whether we have gotten the links where the specific information of housing estate comes from. If not,
        then try to get the links from the files saved in the .doc/link
        Args:
            city: the city we will check whether we have gotten the link list
    '''
    def ensureLinks(self,city):
        if not city in self.linkDict.keys() or len(self.linkDict[city])<1:
            print(True)
            with open("./doc/link/"+city+".txt","r",encoding="utf-8") as f:
                linkList = []
                lines = list(f)
                for line in lines:
                    linkList.append(line.split("\n")[0])
                self.linkDict[city] = linkList
                print("ensureLinks:",self.linkDict[city])
    '''
        crawl the page with specific information of housing estate,and save data in ./doc/data.xlsx
        Args:
            link: the link of the page we intend to crawl
            city: the city we intend to crawl
    '''
    def getDetailPage(self,link,city):
        cityDict=self.cityDict
        regionOne = self.cityDict[city]
        print(regionOne)
        count = 0
        others = False
        cityFromURL= link.split("//")[1].split(".")[0]
        others = (city!=cityFromURL)
        pageLinks=[]
        while count <5:
            try:
                responseOne = requests.get(link,verify=False)
                soup_one =    BeautifulSoup(responseOne.text,"lxml")
                numOfPage = eval(soup_one.find_all("div",attrs={"class":"page-box house-lst-page-box"})[0]["page-data"])["totalPage"]
                urlCity =link.split("//")[1].split(".")[0]
                whetherOther = (urlCity!=city)
                for i in range(1,numOfPage+1):
                    linkDetail = link+ "pg"+str(i)
                    responseDetail =  requests.get(linkDetail,verify=False)
                    soup_detail =  BeautifulSoup(responseDetail.text,"lxml")
                    soupDetailList  = soup_detail.find("ul",attrs={"class":"listContent"}).find_all("li")
                    m = 0
                    for li in soupDetailList:
                        m = m+1
                        pageLink = li.find("div",attrs={"class":"title"}).find("a")["href"]
                        if not pageLink in pageLinks:
                            pageLinks.append(pageLink)
                            title = None
                            title = li.find("div",attrs={"class":"title"}).text.strip()
                            positionInfo= li.find("div",attrs={"class":"positionInfo"}).text.replace(" ","").replace("\n","").split("\xa0")
                            typeOfHouse = None
                            regionTwo = positionInfo[0].strip()
                            regionThree = positionInfo[1].strip()
                            typeOfHouse = positionInfo[2]
                            if typeOfHouse.startswith("/"):
                                typeOfHouse = typeOfHouse[1:]
                            if typeOfHouse.endswith("/"):
                                typeOfHouse = typeOfHouse[:-1]
                            if len(typeOfHouse) == 0:
                                typeOfHouse = "未知类型"
                            if len(positionInfo)== 4:
                                buildYear = positionInfo[3].split("年")[0]
                            else:
                                buildYear = "未知"
                            price = li.find("div",attrs={"class":"totalPrice"}).find("span").text.strip()
                            row = [regionOne,regionTwo,regionThree,others,title,typeOfHouse,buildYear,price]
                            print(row)
                            self.write_sheet.append(row)
            except Exception as e:
                count = count+1
                if count == 5:
                    with open('./doc/error/error.txt',"a+",encoding="utf-8") as ferr:
                        ferr.write("出错的链接是"+link+"，错误的原因是"+str(e)+"\n")
                    with open('./doc/error/errLink.txt',"a+",encoding="utf-8") as ferrLink:
                        ferrLink.write(link+"\n")
            else:
                break
        print("正在保存文件")
        self.wb.save("./doc/data.xlsx")

    '''
        crawl all the pages in the cityList
    '''
    def getDetail(self):
        print("开始加载excel")
        self.wb = load_workbook("./doc/data.xlsx")
        self.write_sheet = self.wb['Sheet1']
        for city in self.cityList:
            self.ensureLinks(city)
            if city in self.linkDict.keys():
                linkList = self.linkDict[city]
                for link in linkList:
                    self.getDetailPage(link,city)
