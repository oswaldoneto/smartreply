import http

from django.http.response import HttpResponse
from django.views.generic.base import View

from classification.models import Classification
from crm.models import Campanha
from mail.admin import MessageCampaign
from mail.models import Message, MessageClassification
from mail.shortcuts import send
from ml import shortcuts


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


class ClassifyMessageView(View):

    def get(self, request, *args, **kwargs):

        # busca a mensagem no banco de dados pelo id
        message_id = kwargs['id']
        message = Message.objects.get(id=message_id)

        # recupera o primeiro pyload da mensagem
        text = message.payload_set.all().first().payload

        # verifica se a mensagem é de alguma campanha
        for campanha in Campanha.objects.all():
            if shortcuts.calculate_similarity(campanha.text, text):
                MessageCampaign.objects.create(message=message, campaign=campanha)

        # pega somente a mensagem de reply
        cleaned_text = self.__clean_original_message(text)

        # realiza a predição de classificação do e-mail
        class_predicted = shortcuts.predict_classification(cleaned_text)
        class_predicted = class_predicted[0]

        # adiciona a classificação no email
        classifications = Classification.objects.filter(name=class_predicted)
        if len(classifications) > 0:
            MessageClassification.objects.create(message=message, classification=classifications.first())

        # muda o status da mensagem para classificado
        message.state = Message.CLASSIFIED
        message.save()

        return HttpResponse()

    def __clean_original_message(self, text):
        cleaned = []
        for line in text.split("\r\n"):
            if not line.startswith(">"):
                cleaned.append(line)
        return "\r\n".join(cleaned)


class RespondMessageView(View):

    def get(self, request, *args, **kwargs):

        # busca a mensagem no banco de dados pelo id
        message_id = kwargs['id']
        message = Message.objects.get(id=message_id)

        # recupera o nome que o email deve ser respondido
        mail_to = message.property_set.filter(key='Return-Path').first()
        mail_to = self.__clean_mail_to(mail_to.value)

        # se o email e de uma campanha
        if message.get_campaign():
            campanha = message.get_campaign()

            if len(message.get_classification()) > 0:

                classification = message.get_classification()[0]

                if (classification.startswith('Proposta')):

                    # envia email de proposta do forum de inteligencia de mercado
                    send(mail_to, campanha, {}, 'a7ca4b05-56cc-4bb9-907c-7926b117824e')


                elif (classification.startswith('Ausencia')):

                    # envia email de ausencia do forum de inteligencia de mercado
                    send(mail_to, campanha, {}, 'ef9401c4-6f2f-475a-853e-62b8b7a5993a')


                elif (classification.startswith('Declinio') or classification.startswith('OptOut')):

                    # envia email de declinio do forum de inteligencia de mercado
                    send(mail_to, campanha, {}, '44e2014f-e50f-4694-bd4a-34b4189daecf')

                elif (classification.startswith('Lixo') or classification.startswith(
                        'Anti-Spam') or classification.startswith('Encaminhar')):

                    # muda o status da mensagem para classificado
                    message.state = Message.FAILURE
                    message.save()

                    return HttpResponse()

        # senão e de campanha
        else:
            pass

        # muda o status da mensagem para classificado
        message.state = Message.ANSWERED
        message.save()

        return HttpResponse()


    def __clean_mail_to(self, mail_to):
        email = ''
        for char in mail_to:
            if char not in " <>":
                email = '%s%s' % (email, char)
        return email










