from elasticsearch.client import Elasticsearch

if __name__ == '__main__':
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    # res = es.get(index="ads", doc_type='ad', id=2)
    res = es.search(index="ads", size=1000, body={"query": {"match_all": {}}})
    for key in res['hits']['hits']:
        print key['_id']
    # print(res['hits'])