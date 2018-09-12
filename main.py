from spiderForLianJia import spiderForLianJia
if __name__ == '__main__':

    #西安,郑州没有小区列表，宁波没有相关数据
    #成都、重庆、沈阳、郑州、南京、上海、杭州、宁波、武汉、长沙、广州、深圳
    cityList = ["xm","su"]
    cityDict  = {"bj":"北京","tj":"天津","qd":"青岛","cd":"成都","cq":"重庆","nj":"南京","sh":"上海","hz":"杭州","wh":"武汉","cs":"长沙","gz":"广州","sz":"深圳","xm":"厦门","su":"苏州"}
    #cityDict  = {"bj":"北京","tj":"天津","qd":"青岛","cd":"成都","cq":"重庆","nj":"南京","sh":"上海","hz":"杭州","wh":"武汉","cs":"长沙","gz":"广州","sz":"深圳"}
    spider = spiderForLianJia(cityList,cityDict)
    spider.getLinks() #获取所有需要爬取的link并且将其保存在doc/link/cityName.txt下
    print("完成getLinks")
    spider.getDetail() #爬取页面，保存信息到doc/data.xlsx
