# 访问openapi
# -*- coding: utf-8 -*-
"""
通过各大厂商的API调用，获取相应API接口返回的json/xml字典
"""

import requests
import json

KEY = 'rmhrne8hal69uwyv'  # API key(私钥)
KEY_amap = '3f4fcab72f1e98f0af9a66fd9826d2b1'
UID = ""  # 用户ID, TODO: 当前并没有使用这个值,签名验证方式将使用到这个值

LOCATION = 'beijing'  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
API = 'https://api.seniverse.com/v3/weather/daily.json'  # API URL，可替换为其他 URL
API_amap = 'https://restapi.amap.com/v3/geocode/geo'  # 阿里高德api
UNIT = 'c'  # 单位
LANGUAGE = 'zh-Hans'  # 查询结果的返回语言
# https://restapi.amap.com/v3/place/around?key=<用户的key>&location=116.473168,39.993015&radius=10000&types=011100
# https://restapi.amap.com/v3/place/around?
# https://restapi.amap.com/v3/place/text?parameters
def fetch_weather(location, start=0, days=15):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT,
        'start': start,
        'days': days
    }, timeout=2)
    return result.json()

# 获取location经纬度值
def get_city_market_location(city, address):
    """
    :param city: 如：北京
    :param address: 规则遵循：国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、大厦，
                    如：北京市朝阳区阜通东大街6号。也可以模糊输入
    :return: locations 该address的经纬度
    """
    result = requests.get(API_amap, params={
        'key': KEY_amap,
        'city': city,
        'address': address
    }, timeout=2)
    # 输出结果为json，将其转为字典格式
    jd = json.loads(result.text)
    # print(jd)
    # 经纬度
    location = jd['geocodes'][0]['location']
    return location

# 获取周边美食
def food_poi(city, address):
    url = "https://restapi.amap.com/v3/place/around?parameters"
    location = get_city_market_location(city, address)
    params = {
        "key": KEY_amap,
        "location": location,   # 需将地址转为经纬度
        "types": "050000",  # 餐饮类型typecode，
        "city": city,   # 可以选择中国大陆境内的不同城市
        "extensions": "all",
        "offset": 25
    }
    result = requests.get(url, params=params)
    result = result.json()['pois']
    food_position_dict = {}
    food_shop = []
    for i in result:
        food_shop.append(i["name"])
    food_position_dict[address] = food_shop
    return food_position_dict


def get_weather_by_day(location, day=1):
    result = fetch_weather(location)
    # print(result["results"][0]["location"])
    normal_result = {
        "location": result["results"][0]["location"],
        "result": result["results"][0]["daily"][day]
    }

    return normal_result


if __name__ == '__main__':
    # default_location = "合肥"
    # result = fetch_weather(default_location)
    # print(json.dumps(result, ensure_ascii=False))
    #
    # default_location = "合肥"
    # result = get_weather_by_day(default_location)
    # print(json.dumps(result, ensure_ascii=False))
    # result = get_city_market_location("杭州", "浙江省杭州市火车南站")
    # print(result)
    result = food_poi("", "浙江省杭州市拱墅区杭行路666号")
    print(result)


