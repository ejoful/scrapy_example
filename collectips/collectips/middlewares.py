# -*- coding: utf-8 -*-

import random
import base64
from settings import PROXIES

import base64
from proxy import GetIp,counter
import logging
ips=GetIp().get_ips()


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
	#print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))



class ProxyMiddleware(object):
    http_n=0     #counter for http requests
    https_n=0    #counter for https requests
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        if request.url.startswith("http://"):
            n=ProxyMiddleware.http_n
            n=n if n<len(ips['http']) else 0
            request.meta['proxy']= "http://%s:%d"%(
                ips['http'][n][0],int(ips['http'][n][1]))
            logging.info('Squence - http: %s - %s'%(n,str(ips['http'][n])))
            ProxyMiddleware.http_n=n+1

        if request.url.startswith("https://"):
            n=ProxyMiddleware.https_n
            n=n if n<len(ips['https']) else 0
            request.meta['proxy']= "https://%s:%d"%(
                ips['https'][n][0],int(ips['https'][n][1]))
            logging.info('Squence - https: %s - %s'%(n,str(ips['https'][n])))
            ProxyMiddleware.https_n=n+1