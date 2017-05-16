#!/usr/bin/python3
# -*- coding: utf-8 -*-
import http.client
import sys
from time import sleep

from smartreply.settings import SITE_END_POINT, SITE_PORT


def main(args):
    print('Initializing smartreply cron script...')
    while(True):

        print('30 seconds sleep')
        sleep(30)

        conn = http.client.HTTPConnection(SITE_END_POINT, SITE_PORT)

        print('HTTP GET /exchange/fetchall')
        conn.request('GET', '/exchange/fetchall')

        print('HTTP GET /processor/new')
        conn.request('GET', '/processor/new')


if __name__ == '__main__':
    main(sys.argv)

