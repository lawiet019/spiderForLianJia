import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
cityDict={"bj":"北京"}
city = "bj"
regionOne = cityDict[city]
link = "https://bj.lianjia.com/xiaoqu/andingmen/"
count = 0
wb = load_workbook("data.xlsx")
write_sheet = wb['Sheet1']
others = False
cityFromURL= link.split("//")[1].split(".")[0]
others = (city!=cityFromURL)
pageLinks=[]
while count <5:
    try:
        responseOne = requests.get(link)
        soup_one =    BeautifulSoup(responseOne.text,"lxml")
        numOfPage = eval(soup_one.find_all("div",attrs={"class":"page-box house-lst-page-box"})[0]["page-data"])["totalPage"]
        urlCity =link.split("//")[1].split(".")[0]
        whetherOther = (urlCity!=city)
        for i in range(1,numOfPage+1):
            linkDetail = link+ "pg"+str(i)
            print(linkDetail)
            responseDetail =  requests.get(linkDetail)
            soup_detail =  BeautifulSoup(responseDetail.text,"lxml")
            soupDetailList  = soup_detail.find("ul",attrs={"class":"listContent"}).find_all("li")
            for li in soupDetailList:
                pageLink = li.find("div",attrs={"class":"title"}).find("a")["href"]
                if not pageLink in pageLinks:
                    pageLinks.append(pageLink)
                    title = None
                    title = li.find("div",attrs={"class":"title"}).text.strip()

                    positionInfo= li.find("div",attrs={"class":"positionInfo"}).text.replace(" ","").replace("\n","").split("\xa0")
                    regionTwo = positionInfo[0].strip()
                    regionThree = positionInfo[1].strip()
                    typeOfHouse = positionInfo[2]
                    if typeOfHouse.startswith("/"):
                        typeOfHouse = typeOfHouse[1:]
                    if typeOfHouse.endswith("/"):
                        typeOfHouse = typeOfHouse[:-1]
                    if len(typeOfHouse) == 0:
                        typeOfHouse = "未知类型"
                    buildYear = positionInfo[3].split("年")[0]
                    price = li.find("div",attrs={"class":"totalPrice"}).find("span").text.strip()
                    row = [regionOne,regionTwo,regionThree,others,title,typeOfHouse,buildYear,price]
                    print(row)
                    write_sheet.append(row)
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
wb.save("data.xlsx")
