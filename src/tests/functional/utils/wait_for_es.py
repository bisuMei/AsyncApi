from elasticsearch import Elasticsearch

from tests.functional.utils.backoff import backoff
from tests.functional.settings import config


class FailConnectinonElasticSearch(Exception):
    pass


@backoff(start_sleep_time=1, factor=2, border_sleep_time=20)
def wait_es():    
    es = Elasticsearch(
        hosts=[config.ELASTIC_HOST], 
        port=config.ELASTIC_PORT, 
        verify_certs=True)
    if not es.ping():        
        raise FailConnectinonElasticSearch('Fail connectinon to ElasticSearch')
    

if __name__ == '__main__':
    wait_es()