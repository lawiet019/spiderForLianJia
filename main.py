from spiderForLianJia import spiderForLianJia
if __name__ == '__main__':
    cityList = ["bj"] #修改希望获取城市的列表，内容为url中代表城市的部分
    spider = spiderForLianJia(cityList)
    spider.getLinks() #获取所有需要爬取的link并且将其保存在doc/link/cityName.txt下
    spider.getDetail() #爬取页面，保存信息到doc/data.xlsx
