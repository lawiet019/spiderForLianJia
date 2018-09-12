import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
cityDict={"bj":"北京"}
city = "bj"
regionOne = cityDict[city]
link = "https://zz.fang.lianjia.com/loupan/jinshui/#jinshui"
count = 0
# wb = load_workbook("data.xlsx")
# write_sheet = wb['Sheet1']
others = False
cityFromURL= link.split("//")[1].split(".")[0]
others = (city!=cityFromURL)
pageLinks=[]
while count <5:
    try:
        responseOne = requests.get(link)
        soup_one =    BeautifulSoup(responseOne.text,"lxml")
        value = int(soup_one.find("span",attrs={"class":"value"}).text)
        numOfPage = value // 10 + 1
        print(numOfPage)
        urlCity =link.split("//")[1].split(".")[0]
        whetherOther = (urlCity!=city)

        for i in range(1,numOfPage+1):
            linkDetail = link.split("#")[0]+ "pg"+str(i)+"/#"+link.split("#")[1]
            print(linkDetail)
            responseDetail =  requests.get(linkDetail)
            soup_detail =  BeautifulSoup(responseDetail.text,"lxml")
            soupDetailList  = soup_detail.find_all("li",attrs={"class":"resblock-list"})
            for li in soupDetailList:
                pageLink = li.find("a",attrs={"class":"name"})["href"]
                if not pageLink in pageLinks:
                    pageLinks.append(pageLink)
                    title = None
                    title = li.find("a",attrs={"class":"name"}).text.strip()
                    regions =  li.find("div",attrs={"class":"resblock-location"}).find_all("span")
                    regionTwo = regions[0].text
                    regionThree =  regions[1].text
                    typeOfHouse = "未获取"
                    buildYear = "未获取"
                    price = li.find("span",attrs={"class":"number"}).text
                    row = [regionOne,regionTwo,regionThree,others,title,typeOfHouse,buildYear,price]
                    print(row)
                    # write_sheet.append(row)
    except Exception as e:
        print(e)
        # count = count+1
        # if count == 5:
        #     with open('./doc/error/error.txt',"a+",encoding="utf-8") as ferr:
        #         ferr.write("出错的链接是"+link+"，错误的原因是"+str(e)+"\n")
        #     with open('./doc/error/errLink.txt',"a+",encoding="utf-8") as ferrLink:
        #         ferrLink.write(link+"\n")
    else:
        break
print("正在保存文件")
