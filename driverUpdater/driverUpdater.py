#!/usr/bin/env python3

import sys

from pprint import pprint as pp

import requests
import dns.resolver # NOTE: dnspython package
import tldextract

class CustomAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, nameservers):
        self.nameservers = nameservers
        super().__init__()

    def resolve(self, host, nameservers, record_type):
        dns_resolver = dns.resolver.Resolver()
        dns_resolver.nameservers = nameservers
        answers = dns_resolver.query(host, record_type)
        for rdata in answers:
            return str(rdata)

    def get_connection(self, url, proxies=None):
        ext = tldextract.extract(url)
        fqdn = ".".join([ ext.subdomain, ext.domain, ext.suffix ])

        print("FQDN: {}".format(fqdn))
        a_record = self.resolve(fqdn, nameservers, 'A')
        print("A record: {}".format(a_record))

        resolved_url = url.replace(fqdn, a_record) # NOTE: Replace first occurrence only
        print("Resolved URL: {}".format(resolved_url))

        return super().get_connection(resolved_url, proxies=proxies)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: {} <url>".format(sys.argv[0]))
        sys.exit(0)

    url = sys.argv[1]

    nameservers = [
        '208.67.222.222', # NOTE: OpenDNS
        '8.8.8.8'         # NOTE: Google
    ]

    session = requests.Session()
    session.mount(url, CustomAdapter(nameservers))

    parameters = {
        # "headers": {'Content-Type': 'application/json'},
        # "timeout" : 45,
        # "stream" : True
        # "proxies" : {
        #   "http": "http://your_http_proxy:8080/",
        #   "https": "http://your_https_proxy:8081/"
        # },
        # "auth": (name, password),
        # ...
    }

    response = session.get(url, **parameters)
    pp(response.__dict__)