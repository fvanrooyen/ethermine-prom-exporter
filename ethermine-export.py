#!/usr/bin/env python

from prometheus_client import start_http_server, Gauge, Counter
import argparse
import httplib
import time
import collections
import json
import requests

version = 0.50

REQUEST_ADDRESS = Gauge('Ethermine_Address','Etermine Address',['MinerID'])
REQUEST_REPORTED_HASH = Gauge('Ethermine_Reported_Hash_Rate', 'Ethermine Reported Hash Rate')
REQUEST_UNPAID_BALANCE = Gauge('Ethermine_Unpaid_Balance', 'Ethermine Unpaid Balance')
REQUEST_PROGRESS_PAYOUT = Gauge('Ethermine_Progress_Payout', 'Ethermine Payout Progress')
REQUEST_ACTIVE_WORKERS= Gauge('Ethermine_Active_Workers', 'Ethermine Active Workers')

if __name__ == "__main__":
    r = requests.get('https://ethermine.org/api/miner_new/5526624c135c0390b5b5EE0aC5A2063Fe19F9FD5')
    data = json.loads(r.text)
    REQUEST_ADDRESS.labels(data["address"])
    print(data["address"])
    hashrate = data["reportedHashRate"]
    hashrate = hashrate.split()
    REQUEST_REPORTED_HASH.set(hashrate[0])
    print(hashrate[0])
    REQUEST_UNPAID_BALANCE.set(float(data['unpaid']) / 1000000000000000000)
    print(float(data['unpaid']) / 1000000000000000000) 
    REQUEST_PROGRESS_PAYOUT.set((float(data['unpaid']) / 10000000000000000)/.5)
    print((float(data['unpaid']) / 10000000000000000)/.5)
    REQUEST_ACTIVE_WORKERS.set(data["minerStats"]["activeWorkers"])
    print(data["minerStats"]["activeWorkers"])
