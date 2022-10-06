FROM staticfloat/nginx-certbot

COPY *.conf /etc/nginx/conf.d/
COPY --chown=www-data:www-data html/* /var/www/html/

COPY init.sh /scripts/

ENV DOMAIN="oddcron.ninja"
ENV C2IP="18.232.136.101"
ENV CERTBOT_EMAIL="movveworks@gmail.com"

CMD ["/bin/bash", "/scripts/init.sh"]