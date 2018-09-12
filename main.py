from spiderForAnJuKe import spiderForAnJuKe
if __name__ == '__main__':
    cityList = ["nb"]
    for city in cityList:
        spider = spiderForAnJuKe(city,"宁波")
        spider.getErShouFangArea()
        spider.getErShouFang()
