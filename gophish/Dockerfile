FROM golang:1.18.0 as go-build

ENV GOPHISH_VERSION v0.12.1

RUN apt-get update && apt-get install -y unzip python3 python3-pip

RUN wget https://github.com/gophish/gophish/releases/download/${GOPHISH_VERSION}/gophish-${GOPHISH_VERSION}-linux-64bit.zip

RUN unzip gophish-${GOPHISH_VERSION}-linux-64bit.zip

COPY files/* ./

RUN mkdir email_templates

COPY email_templates/* ./email_templates/

EXPOSE 3333 

EXPOSE 80

EXPOSE 443

CMD ["/bin/bash", "init.sh"]

# RUN ["chmod", "+x", "/go/gophish", "/go/change_password.py", "/go/run-gophish.sh"]

# RUN ["./run-gophish.sh"]

# RUN ["pip3","install","-r", "requirements.txt"]

# # RUN ["chmod", "+x", "/go/change_password.py"]

# # RUN ["./change_password.py"]