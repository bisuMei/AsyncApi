import logging
import sys
import time 

import redis 

from tests.functional.settings import config


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


while True:
    try:
        re = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, socket_connect_timeout=1)    
        re.ping()
        logger.info("Success connect to redis")
        break           
    except redis.exceptions.ConnectionError:        
        logger.info("Establishing connection to redis...")
        time.sleep(0.5)