FROM staticfloat/nginx-certbot

RUN apt-get update && apt-get install -y python3 python3-pip 

COPY *.conf /etc/nginx/conf.d/
COPY --chown=www-data:www-data html/* /var/www/html/

COPY /scripts/* /scripts/

ENV DOMAIN="oddcron.ninja"
#ENV C2IP="127.0.0.1"
ENV C2IP="167.71.16.171"

ENV CERTBOT_EMAIL="movveworks@gmail.com"

EXPOSE 443

CMD ["/bin/bash", "/scripts/init.sh"]