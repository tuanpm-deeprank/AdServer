import ast
import math
from elasticsearch.client import Elasticsearch
from util import load_vocabs, ads_by_content_v4, convert_str_2_vec
from datetime import datetime


def getAd(adId):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    res = es.get(index="ads", doc_type='ad', id=adId)
    ad = dict()
    ad['title'] = res['_source']['title']
    ad['image'] = res['_source']['link']
    ad['price'] = res['_source']['price']
    return ad

def getAdsIdList(content):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    res = es.search(index="ads", size=1000, body={"query": {"match_all": {}}})
    ads = dict()
    for key in res['hits']['hits']:
        ads[key['_id']] = dict()
        ads[key['_id']]['feature'] = ast.literal_eval(key['_source']['feature'])
        ads[key['_id']]['square'] = key['_source']['square']
    vocabs = load_vocabs()
    ads_list = ads_by_content_v4(content, vocabs, ads, 3)
    return ads_list

def getAdsList(content):
    adsIdLst = getAdsIdList(content)
    adsList = []
    for i in adsIdLst:
        adsList.append(getAd(i))
    context = {
        'adList': adsList
    }
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + content
    return  adsList

def insert_ads_2_db(ads):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    vocabs = load_vocabs()
    title = ads['title'].strip()
    price = ads['price'].strip()
    link = ads['image'].strip()
    description = ads['description'].strip()
    t = convert_str_2_vec(description, vocabs)
    feature = str(t)
    square = 0.0
    for w in t.keys():
        square += math.pow(t[w], 2)
    doc = {
        'title': title,
        'price': price,
        'link': link,
        'description': description,
        'feature': feature,
        'square': square,
    }
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + doc['title']
    adId = current_max_id()+1
    res = es.index(index="ads", doc_type='ad', id=adId, body=doc)

def current_max_id():
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    res = es.search(index="ads", doc_type='ad', body={"aggs": {"max_id": {"max": {"field": "id"}}}, "size": 0})
    return res['hits']['total']

if __name__ == '__main__':
    current_max_id()
