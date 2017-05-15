from django.db import models

from mail.models import EmailMessage


class Token(models.Model):
    word = models.CharField(max_length=100)


class Occurrence(models.Model):
    token = models.ForeignKey(Token)
    message = models.ForeignKey(EmailMessage)
    incidence = models.IntegerField()

