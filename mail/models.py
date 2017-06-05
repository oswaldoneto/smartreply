from django.db import models

from classification.models import Classification
from crm.models import Campanha
from exchange.models import EmailServer


class Message(models.Model):
    NEW = '1'
    PROCESSING = '2'
    CLASSIFIED = '3'
    ANSWERED = '4'
    FAILURE = '5'
    STATE = (
        (NEW, 'NEW'),
        (PROCESSING, 'PROCESSING'),
        (CLASSIFIED, 'CLASSIFIED'),
        (ANSWERED, 'ANSWERED'),
        (FAILURE, 'FAILURE'),
    )
    server = models.ForeignKey(EmailServer)
    uuid = models.IntegerField()
    state = models.CharField(max_length=1, choices=STATE, default=NEW)
    time = models.DateTimeField(auto_now_add=True)

    def get_from(self):
        email_from = self.property_set.filter(key='From')
        return email_from.first().value if len(email_from) > 0 else None

    def get_subject(self):
        email_subject = self.property_set.filter(key='Subject')
        return email_subject.first().value if len(email_subject) > 0 else None

    def get_body(self):
        body = self.payload_set.all()
        return body.first().payload if len(body) > 0 else None

    def get_campaign(self):
        return self.messagecampaign_set.first().campaign.name if len(self.messagecampaign_set.all()) > 0 else None

    def get_classification(self):
        return [cls.classification.name for cls in self.messageclassification_set.all()]


class Property(models.Model):
    message = models.ForeignKey(Message)
    key = models.CharField(max_length=255)
    value = models.TextField()


class Payload(models.Model):
    message = models.ForeignKey(Message)
    payload = models.TextField()


class MessageClassification(models.Model):
    message = models.ForeignKey(Message)
    classification = models.ForeignKey(Classification)


class MessageCampaign(models.Model):
    message = models.ForeignKey(Message)
    campaign = models.ForeignKey(Campanha)





