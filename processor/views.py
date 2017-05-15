import http

from django.http.response import HttpResponse
from django.views.generic.base import View

from classification.models import Classification
from mail.models import Message
from mail.shortcuts import send
from ml.shortcuts import predict


class NewMessageView(View):

    def get(self, request, *args, **kwargs):
        message_ids = []
        for m in Message.objects.filter(state=Message.NEW):
            #m.state = Message.PROCESSING
            #m.save()
            message_ids.append(m.id)
        for id in message_ids:
            conn = http.client.HTTPConnection('localhost', 8000)
            conn.request('GET', '/processor/message/%s' % id)

        return HttpResponse()


class MessageView(View):

    def get(self, request, *args, **kwargs):

        message_id = kwargs['id']

        message = Message.objects.get(id=message_id)

        text = message.payload_set.all().first().payload

        class_predicted = predict(text)

        classification = Classification.objects.filter(name=class_predicted[0]).first()

        template_id = classification.property_set.filter(name='template-id').first().value

        send()

        return HttpResponse()


















