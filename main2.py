from spiderForNewHouse import spiderForNewHouse
if __name__ == '__main__':
    cityList = ["nb"]
    for city in cityList:
        spider = spiderForNewHouse(city,"宁波")
        spider.getErShouFangArea()
        spider.getErShouFang()
