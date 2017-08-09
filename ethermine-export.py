#!/usr/bin/env python

from prometheus_client import start_http_server, Gauge, Counter
#from prometheus_client import start_http_server, Metric, REGISTRY
import argparse
import httplib
import time
import collections
import json
import requests

version = 0.50

REQUEST_ADDRESS = Gauge('Ethermine Address','Etermine Address')
REQUEST_REPORTED_HASH = Gauge('Ethermine Reported Hash Rate', 'Ethermine Reported Hash Rate')
REQUEST_UNPAID_BALANCE = Gauge('Ethermine Unpaid Balance', 'Ethermine Unpaid Balance')
REQUEST_MINER_STATS = Gauge('Ethermine Miner Stats', 'Ethermine Miner Stats')
REQUEST_ACTIVE_WORKERS= Gauge('Ethermine Active Workers', 'Ethermine Active Workers')

if __name__ == "__main__":
    r = requests.get('https://ethermine.org/api/miner_new/5526624c135c0390b5b5EE0aC5A2063Fe19F9FD5')
    data = json.loads(r.text)
    print(data["address"])
    print(data["reportedHashRate"])
    print(float(data['unpaid']) / 1000000000000000000)
    print((float(data['unpaid']) / 10000000000000000)/.5)
    print(data["minerStats"]["activeWorkers"])
