from spiderForErShouFang import spiderForErShouFang
if __name__ == '__main__':
    cityList = ["zz","xa"]
    #西安,郑州没有小区列表，宁波没有相关数据
    #成都、重庆、沈阳、郑州、南京、上海、杭州、宁波、武汉、长沙、广州、深圳

    cityDict  = {"zz":"郑州","xa":"西安"}
    spider = spiderForErShouFang(cityList,cityDict)
    spider.getLinks() #获取所有需要爬取的link并且将其保存在doc/link/cityName.txt下
    spider.getDetail() #爬取页面，保存信息到doc/data.xlsx
    spider.getNewLinks()
    spider.getNewDetail()
