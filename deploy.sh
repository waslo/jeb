#!/bin/bash

cd /home/ubuntu/jeb
git pull origin master
kill $(ps aux | grep 'jeb.py' | awk '{print $2}')
echo "Running new version of Jeb!"
python3 jeb.py > ./log &
