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
            m.state = Message.PROCESSING
            m.save()
            message_ids.append(m.id)
        for id in message_ids:
            http_post = request.environ['HTTP_HOST'].split(':')
            host = http_post[0]
            if len(http_post) > 1:
                port = http_post[1]
            else:
                port = 80
            conn = http.client.HTTPConnection(host, port)
            conn.request('GET', '/processor/message/%s' % id)

        return HttpResponse()


class MessageView(View):

    def get(self, request, *args, **kwargs):
        message_id = kwargs['id']

        message = Message.objects.get(id=message_id)

        text = message.payload_set.all().first().payload

        class_predicted = predict(text)

        classification = Classification.objects.filter(name=class_predicted[0]).first()

        mail_to = message.property_set.filter(key='Return-Path').first()

        substitution = {
            '%email_from%': mail_to.value[1:len(mail_to.value) - 1],
            '%email_body%': text,
            '%classification%': class_predicted[0],
        }
        send(mail_to.value, 'Resposta Automática POC Machine Learning', substitution)

        message.state = Message.TREATED
        message.save()

        return HttpResponse()
