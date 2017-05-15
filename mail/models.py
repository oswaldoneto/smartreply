from django.db import models

from exchange.models import EmailServer


class Message(models.Model):
    NEW = '1'
    PROCESSING = '2'
    TREATED = '3'
    STATE = (
        (NEW, 'NEW'),
        (PROCESSING, 'PROCESSING'),
        (TREATED, 'TREATED'),
    )
    server = models.ForeignKey(EmailServer)
    uuid = models.IntegerField()
    state = models.CharField(max_length=1, choices=STATE, default=NEW)


class Property(models.Model):
    message = models.ForeignKey(Message)
    key = models.CharField(max_length=255)
    value = models.TextField()


class Payload(models.Model):
    message = models.ForeignKey(Message)
    payload = models.TextField()





