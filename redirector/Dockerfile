FROM staticfloat/nginx-certbot

ARG AWS_DEFAULT_REGION
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION

ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID

ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

RUN apt-get update && apt-get install -y python3 python3-pip awscli

COPY *.conf /etc/nginx/conf.d/
COPY --chown=www-data:www-data html/* /var/www/html/

COPY /scripts/ /scripts/

RUN pip3 install --upgrade awscli

RUN pip3 install -r scripts/redirector_ip/requirements.txt

# RUN python3 scripts/update-ip-address.py -d oddcron.ninja -u andross561

ENV DOMAIN="oddcron.ninja"
#ENV C2IP="127.0.0.1"
ENV C2IP="167.71.16.171"

ENV CERTBOT_EMAIL="movveworks@gmail.com"

EXPOSE 80

EXPOSE 443

CMD ["/bin/bash", "/scripts/init.sh"]