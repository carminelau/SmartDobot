import time
import requests

i=0
for i in range(3):
    req = requests.get ("http://192.168.1.102:5000/avviarullo?speed=0.29&direction=1")
    time.sleep(14.9)
    req = requests.get ("http://192.168.1.102:5000/avviarullo?speed=0.29&direction=-1")
    time.sleep(14.9)
    print(i)
    i=i+1

req = requests.get ("http://192.168.1.102:5000/avviarullo?speed=0&direction=1")