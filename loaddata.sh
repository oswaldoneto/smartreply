#!/bin/sh
python manage.py loaddata exchange/fixture/emailserver.json
python manage.py loaddata exchange/fixture/mailbox.json


