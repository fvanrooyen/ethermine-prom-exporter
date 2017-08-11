#!/usr/bin/env python

from prometheus_client import start_http_server, Gauge, Counter
import argparse
import json
import requests
import time
import logging
import logging.handlers

version = 0.50

# Parse commandline arguments
parser = argparse.ArgumentParser(description="EtherminePrometheus exporter v" + str(version))
parser.add_argument("-m", "--miner", metavar="<mid>", required=True, help="Miner Address")
parser.add_argument("-p", "--port", metavar="<port>", required=False, help="Port for listenin", default=8701, type=int)
parser.add_argument("-f", "--frequency", metavar="<seconds>", required=False, help="Interval in seconds between checking measures", default=60, type=int)
args = parser.parse_args()

#Get the Arguments
mineraddress = args.miner
listenport = args.port
sleep_time = args.frequency

#Setup Logger
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/var/run/syslog')
my_logger.addHandler(handler)

#Prometheus Requests 
REQUEST_ADDRESS = Gauge('Ethermine_Address','Etermine Address',['MinerID'])
REQUEST_REPORTED_HASH = Gauge('Ethermine_Reported_Hash_Rate', 'Ethermine Reported Hash Rate')
REQUEST_UNPAID_BALANCE = Gauge('Ethermine_Unpaid_Balance', 'Ethermine Unpaid Balance')
REQUEST_PROGRESS_PAYOUT = Gauge('Ethermine_Progress_Payout', 'Ethermine Payout Progress')
REQUEST_ACTIVE_WORKERS= Gauge('Ethermine_Active_Workers', 'Ethermine Active Workers')

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(listenport)

    while True:
        
        #Check to see if Ethermine is up
        try:
            r = requests.get('https://ethermine.org/api/miner_new/' + mineraddress)
        except requests.exceptions.RequestException as e:
                my_logger.critical(e)

        #Check to see if there are issues with the API 
        if r.text != 'Too many requests, please try again later.':
            data = json.loads(r.text)
            REQUEST_ADDRESS.labels(data["address"])
            hashrate = data["reportedHashRate"]
            hashrate = hashrate.split()
            REQUEST_REPORTED_HASH.set(hashrate[0])
            REQUEST_UNPAID_BALANCE.set(float(data['unpaid']) / 1000000000000000000)
            REQUEST_PROGRESS_PAYOUT.set((float(data['unpaid']) / 10000000000000000)/.5)
            REQUEST_ACTIVE_WORKERS.set(data["minerStats"]["activeWorkers"])

        #If the Frequency is too aggressive then add 5 second to the time and wait for counters to reset
        else:
            logging.warning('Frequency too aggresive need to backoff')
            sleep_time = sleep_time + 5
            time.sleep(300)

        #Sleep before run again
        time.sleep(sleep_time)