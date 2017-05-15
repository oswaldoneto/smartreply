from django.db import models

# Create your models here.

class EmailServer(models.Model):
    host = models.CharField(max_length=255)
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    active = models.BooleanField()

    def __unicode__(self):
        return str(self.host)


class MailBox(models.Model):
    mailbox = models.CharField(max_length=100)
    server = models.ForeignKey(EmailServer)
    active = models.BooleanField()
