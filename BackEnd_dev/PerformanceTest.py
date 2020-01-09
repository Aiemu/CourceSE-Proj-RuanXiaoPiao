import requests
import json

from time import time

url = 'http://62.234.50.47/getActivityInfo/'
data = {'activity_id': 2};

print('Requests sending...')
start = time()
cut_up = time()

for i in range(0, 1000):
    requests.post(url, data=json.dumps(data))

    if (i + 1) % 100 == 0: 
        cut_down = time()
        print('Time for requests from', i - 99, 'to', i, ':', cut_down - cut_up)
        cut_up = time()


end = time()

print('Total time for 1000 requests:', end - start)