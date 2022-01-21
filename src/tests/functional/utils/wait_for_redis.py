import redis
import time


while True:
    try:
        rc = redis.StrictRedis(host='redis_test', port=6379, db=0)    
        gdata = rc.hgetall('global')   
        print('Connected to redis service')     
        break
    except redis.exceptions.ConnectionError:
        time.sleep(0.5)        
        print('wait')


