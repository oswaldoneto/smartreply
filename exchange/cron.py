import http.client
import sys
from time import sleep


def main(args):
    while(True):

        conn = http.client.HTTPConnection('localhost', 8000)
        conn.request('GET', '/exchange/fetchall')
        print('HTTP GET /exchange/fetchall')

        sleep(10)




if __name__ == '__main__':
    main(sys.argv)

