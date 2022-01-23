import logging
import sys
import time 

from elasticsearch import Elasticsearch

from tests.functional.settings import config


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


while True:
    es = Elasticsearch(hosts=[config.ELASTIC_HOST], port=config.ELASTIC_PORT)
    if es.ping():
        logger.info("Success connect to elastic")
        break
    else:
        time.sleep(0.5)
        logger.info("Establishing connection to elastic...")