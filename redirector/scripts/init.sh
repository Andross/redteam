#!/bin/bash

python3 scripts/redirector_ip/update_ip_address.py -d oddcron.ninja -u andross561

python3 scripts/redirector_ip/check_ip.py -d oddcron.ninja

sed -i /etc/nginx/conf.d/*.conf -e "s/__DOMAIN__/$DOMAIN/g"
sed -i /etc/nginx/conf.d/*.conf -e "s/__IP__/$C2IP/g"

/scripts/entrypoint.sh