#!/bin/sh
echo "Seeding /dev/random"
haveged -f /dev/random
dockerd --iptables=false  >> /var/log/dockerd.log &
cd app 
python3 enclave_server.py
