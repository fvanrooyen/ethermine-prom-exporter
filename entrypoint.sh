#!/bin/bash

if [ -z "$MINER" ]; then
        echo "Miner address is required"
        exit -1
fi

if [ -z "$FREQUENCY"]; then
    FREQUENCY=60
fi

if [ -z "$LISTENPORT" ]; then
    LISTENPORT=8701
fi

python /usr/local/bin/ethermine-export.py -m $MINER -f $FREQUENCY -p $LISTENPORT