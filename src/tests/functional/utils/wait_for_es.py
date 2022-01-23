import time 

from elasticsearch import Elasticsearch

from tests.functional.settings import config


while True:
    es = Elasticsearch(hosts=[config.ELASTIC_HOST], port=config.ELASTIC_PORT)
    if es.ping():
        print("Success connect to elastic")
        break
    else:
        time.sleep(0.5)
        print("Establishing connection to elastic...")