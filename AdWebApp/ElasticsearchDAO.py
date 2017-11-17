import ast

from elasticsearch.client import Elasticsearch
from AdWebApp.models import Ad
from util import load_vocabs, ads_by_content_v4

def getAd(adId):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    res = es.get(index="ads", doc_type='ad', id=adId)
    ad = Ad()
    ad.title = res['_source']['title']
    ad.link = res['_source']['link']
    ad.price = res['_source']['price']
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
    return adsList