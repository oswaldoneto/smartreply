#!/bin/sh
python manage.py dumpdata --indent 2 --format=json exchange.emailserver > exchange/fixture/emailserver.json
python manage.py dumpdata --indent 2 --format=json exchange.mailbox > exchange/fixture/mailbox.json
