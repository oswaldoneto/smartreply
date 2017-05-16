#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# -*- coding: utf-8 -*-
import http.client
import sys
from time import sleep


def main(args):
    print('Initializing smartreply cron script...')
    while(True):

        print('30 seconds sleep')
        sleep(30)

        print('HTTP GET /exchange/fetchall')
        conn = http.client.HTTPConnection('localhost', 8000)
        conn.request('GET', '/exchange/fetchall')

        print('HTTP GET /processor/new')
        conn = http.client.HTTPConnection('localhost', 8000)
        conn.request('GET', '/processor/new')


if __name__ == '__main__':
    main(sys.argv)

