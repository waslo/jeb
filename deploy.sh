#!/bin/bash

cd /home/ubuntu/jeb
git pull origin master
pip3 install -r requirements.txt

# Kill the existing process
kill $(ps aux | grep 'jeb.py' | awk '{print $2}')

echo "Running new version of Jeb!"
python3 jeb.py > ./log &
