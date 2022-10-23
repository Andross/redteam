import requests

def get_public_ip():
    r = requests.get('http://ip.me/')
    public_ip = r.content.decode('utf-8')
    return public_ip