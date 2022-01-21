import requests
import time

while True:
    try:
        res = requests.head('http://elasticsearch_test:9200')
        print('Connected to elasticsearch service')
        break        
    except requests.exceptions.ConnectionError:
        time.sleep(0.5)
        print('wait')