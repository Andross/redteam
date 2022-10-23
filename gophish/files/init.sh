#!/bin/bash

chmod +x gophish setup-gophish.py

./gophish &

pip3 install -r requirements.txt

./setup-gophish.py && pkill -f gophish

./gophish