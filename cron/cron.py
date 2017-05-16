#!/usr/bin/python3
# -*- coding: utf-8 -*-
import http.client
import sys
from time import sleep

from django.conf import settings


def main(args):
    print('Initializing smartreply cron script...')
    while(True):

        print('30 seconds sleep')
        sleep(30)


        site_endpoint = getattr(settings, 'SITE_ENDPOINT', False)
        site_port = getattr(settings, 'SITE_END_POINT', False)
        if not site_endpoint :
            raise Exception('site_endpoint is missing')
        if not site_port :
            raise Exception('site_port is missing')


        conn = http.client.HTTPConnection(site_endpoint, site_port)

        print('HTTP GET /exchange/fetchall')
        conn.request('GET', '/exchange/fetchall')

        print('HTTP GET /processor/new')
        conn.request('GET', '/processor/new')


if __name__ == '__main__':
    main(sys.argv)

