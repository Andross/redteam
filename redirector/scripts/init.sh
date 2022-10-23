#!/bin/bash

pip3 install -r requirements.txt

python3 update-ip-address.py -d oddcron.ninja -u andross561

sed -i /etc/nginx/conf.d/*.conf -e "s/__DOMAIN__/$DOMAIN/g"
sed -i /etc/nginx/conf.d/*.conf -e "s/__IP__/$C2IP/g"

/scripts/entrypoint.sh