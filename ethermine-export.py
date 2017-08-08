#!/usr/bin/env python

from prometheus_client import start_http_server, Gauge, Counter
import argparse
import httplib
import time
import collections
import json
import socket

version = 0.50

# Check if IP is valid
def validIP(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except socket.error:
        parser.error("Invalid IP Address.")
    return ip
