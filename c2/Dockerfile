FROM alpine:3.14

RUN wget https://github.com/BishopFox/sliver/releases/download/v1.5.29/sliver-server_linux

EXPOSE 443

EXPOSE 80

RUN chmod +x sliver-server_linux

CMD ["./sliver-server_linux"]