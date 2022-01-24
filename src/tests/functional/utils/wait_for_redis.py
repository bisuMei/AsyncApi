import redis

from tests.functional.utils.backoff import backoff 
from tests.functional.settings import config


class FailConnectinonRedis(Exception):
    pass


@backoff(start_sleep_time=1, factor=2, border_sleep_time=20)
def wait_redis():    
    try:
        re = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, socket_connect_timeout=1)              
        re.ping()    
    except redis.exceptions.ConnectionError:
        raise FailConnectinonRedis('Fail connectinon to Redis')
    

if __name__ == '__main__':
    wait_redis()