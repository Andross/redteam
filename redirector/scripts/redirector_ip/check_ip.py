import socket, argparse
import time
import dns, dns.name
import dns.query, dns.resolver
from get_public_ip import get_public_ip

parser = argparse.ArgumentParser(description='A python script used to update the IP address for domains you own on name.com')
parser.add_argument('-d','--domain', help='Description for foo argument', required=True)
args = vars(parser.parse_args())

def log(msg):
    with open('check-ip-log.log','a+') as f:
        f.write(msg)


def get_authoritative_nameserver(domain, log=lambda msg: None):
    n = dns.name.from_text(domain)

    depth = 2
    default = dns.resolver.get_default_resolver()
    nameserver = default.nameservers[0]

    last = False
    while not last:
        s = n.split(depth)

        last = s[0].to_unicode() == u'@'
        sub = s[1]

        log('Looking up %s on %s' % (sub, nameserver))
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        response = dns.query.udp(query, nameserver)

        rcode = response.rcode()
        if rcode != dns.rcode.NOERROR:
            if rcode == dns.rcode.NXDOMAIN:
                raise Exception('%s does not exist.' % sub)
            else:
                raise Exception('Error %s' % dns.rcode.to_text(rcode))

        rrset = None
        if len(response.authority) > 0:
            rrset = response.authority[0]
        else:
            rrset = response.answer[0]

        rr = rrset[0]
        if rr.rdtype == dns.rdatatype.SOA:
            log('Same server is authoritative for %s' % sub)
        else:
            authority = rr.target
            log('%s is authoritative for %s' % (authority, sub))
            nameserver = default.query(authority).rrset[0].to_text()

        depth += 1

    return nameserver

tld_nameserver_ip = get_authoritative_nameserver(args['domain'], log)

print("IP of TLD nameserver for {domain} is {ip}".format(domain=args["domain"],ip=tld_nameserver_ip))

my_resolver = dns.resolver.Resolver()

# 8.8.8.8 is Google's public DNS server
my_resolver.nameservers = [tld_nameserver_ip]



while True:
    public_ip = get_public_ip()

    answers = my_resolver.resolve(args['domain'])
    for rdata in answers:
        domain_ip = rdata.address
    log("Public IP is {public_ip} and the IP of {domain} is {domain_ip}".format(public_ip=public_ip, domain=args['domain'],domain_ip=domain_ip))
    time.sleep(5)
    if public_ip.strip() == domain_ip.strip():
        log("IPs match! ({public_ip}:{domain_ip}) Ending".format(public_ip=public_ip, domain_ip=domain_ip))
        break