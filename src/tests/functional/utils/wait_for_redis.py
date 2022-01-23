import time 

import redis 

from tests.functional.settings import config


while True:
    try:
        re = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, socket_connect_timeout=1)    
        re.ping()
        print("Success connect to redis")
        break           
    except redis.exceptions.ConnectionError:        
        print("Establishing connection to redis...")
        time.sleep(0.5)