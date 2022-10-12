#!/bin/bash

chmod +x gophish change_password.py run-gophish.sh 

./gophish &

pip3 install -r requirements.txt

./setup-gophish.py && pkill -f gophish

./gophish