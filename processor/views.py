import http

from django.http.response import HttpResponse
from django.views.generic.base import View

from classification.models import Classification
from crm.models import Campanha, Cliente, Cobranca
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
            conn.request('GET', '/processor/message/%s/classify' % id)

        return HttpResponse()


class ClassifyMessageView(View):

    def get(self, request, *args, **kwargs):

        # busca a mensagem no banco de dados pelo id
        message_id = kwargs['id']
        message = Message.objects.get(id=message_id)

        # recupera o primeiro pyload da mensagem
        text = message.payload_set.all().first().payload

        # verifica se a mensagem é de alguma campanha
        has_campaign = False
        for campanha in Campanha.objects.all():
            if shortcuts.calculate_similarity(campanha.text, text):
                MessageCampaign.objects.create(message=message, campaign=campanha)
                has_campaign = True

        # pega somente a mensagem de reply
        cleaned_text = self.__clean_original_message(text)

        if has_campaign:

            # realiza a predição de classificação do e-mail
            class_predicted = shortcuts.predict_classification(cleaned_text)
            class_predicted = class_predicted[0]

            # adiciona a classificação no email
            classifications = Classification.objects.filter(name=class_predicted)
            if len(classifications) > 0:
                MessageClassification.objects.create(message=message, classification=classifications.first())

        else:

            # Faz a preedição do primeiro contato do usuário
            entrada_predicted = shortcuts.predict_entrada(cleaned_text)
            entrada_predicted = entrada_predicted[0]

            cls = Classification.objects.filter(name=entrada_predicted)
            if len(cls) == 0:
                new_cls = Classification.objects.create(name=entrada_predicted)
            else:
                new_cls = cls.first()
            MessageClassification.objects.create(message=message, classification=new_cls)

            if entrada_predicted.startswith('Informacao'):

                # Faz a preedição do primeiro contato do usuário
                curso_predicted = shortcuts.predict_cursos(cleaned_text)
                curso_predicted = curso_predicted[0]

                cls = Classification.objects.filter(name=curso_predicted)
                if len(cls) == 0:
                    new_cls = Classification.objects.create(name=curso_predicted)
                else:
                    new_cls = cls.first()
                MessageClassification.objects.create(message=message, classification=new_cls)

            if entrada_predicted.startswith('Cobranca'):

                # recupera o nome que o email deve ser respondido
                mail_to = message.property_set.filter(key='Return-Path').first()
                mail_to = self.__clean_mail_to(mail_to.value)

                clientes = Cliente.objects.filter(email=mail_to)

                if len(clientes) > 0:

                    cliente = clientes.first()

                    cob_abertas = Cobranca.objects.filter(cliente=cliente, pago=False)

                    if len(cob_abertas) > 0:

                        cls = Classification.objects.filter(name='Atraso Pagamento')
                        if len(cls) == 0:
                            new_cls = Classification.objects.create(name='Atraso Pagamento')
                        else:
                            new_cls = cls.first()
                        MessageClassification.objects.create(message=message, classification=new_cls)

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


    def __clean_mail_to(self, mail_to):
        email = ''
        for char in mail_to:
            if char not in " <>":
                email = '%s%s' % (email, char)
        return email


class NewRespondMessageView(View):

    def get(self, request, *args, **kwargs):
        message_ids = []
        for m in Message.objects.filter(state=Message.CLASSIFIED):
            message_ids.append(m.id)
        for id in message_ids:
            http_post = request.environ['HTTP_HOST'].split(':')
            host = http_post[0]
            if len(http_post) > 1:
                port = http_post[1]
            else:
                port = 80
            conn = http.client.HTTPConnection(host, port)
            conn.request('GET', '/processor/message/%s/respond' % id)

        return HttpResponse()


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

            if len(message.get_classification()) > 0:

                for classification in message.get_classification():

                    if (classification.startswith('Informacao')):

                        # envia email de proposta do forum de inteligencia de mercado
                        send(mail_to, 'Informacao', {'%MESSAGE_ID%': message_id}, '5f593f6d-fbfa-4070-a11a-a482f47338b6')

                    if (classification.startswith('Cobranca')):

                        if 'Atraso Pagamento' in message.get_classification():

                            clientes = Cliente.objects.filter(email=mail_to)
                            if len(clientes) > 0:
                                cliente = clientes.first()
                                cob_abertas = Cobranca.objects.filter(cliente=cliente, pago=False)

                                if len(cob_abertas) > 0:

                                    subs = {'%NOME%': cliente.nome,
                                            '%BOLETO%': cob_abertas[0].boleto, '%VALOR%': cob_abertas[0].valor }

                                    # envia email de proposta do forum de inteligencia de mercado
                                    send(mail_to, 'Solicitação de Informação de Cobrança', subs,
                                         '9bb4f51b-f961-456a-afc8-360db0eb8db6')


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


class MBAView(View):

    def get(self, request, *args, **kwargs):

        message_id = kwargs['id']
        message = Message.objects.get(id=message_id)

        # recupera o nome que o email deve ser respondido
        mail_to = message.property_set.filter(key='Return-Path').first()
        mail_to = self.__clean_mail_to(mail_to.value)

        # envia email de proposta do forum de inteligencia de mercado
        send(mail_to, 'Informacao MBA', {}, '00ecc17f-e9a4-4696-ad15-0ef6bc348b84')

        return HttpResponse()

    def __clean_mail_to(self, mail_to):
        email = ''
        for char in mail_to:
            if char not in " <>":
                email = '%s%s' % (email, char)
        return email


class CobitView(View):

    def get(self, request, *args, **kwargs):

        message_id = kwargs['id']
        message = Message.objects.get(id=message_id)

        # recupera o nome que o email deve ser respondido
        mail_to = message.property_set.filter(key='Return-Path').first()
        mail_to = self.__clean_mail_to(mail_to.value)

        # envia email de proposta do forum de inteligencia de mercado
        send(mail_to, 'Informacao Cobit', {}, '9e2be2f5-b44a-4246-9a7b-774ce89106ed')

        return HttpResponse()

    def __clean_mail_to(self, mail_to):
        email = ''
        for char in mail_to:
            if char not in " <>":
                email = '%s%s' % (email, char)
        return email


class ScrumView(View):

    def get(self, request, *args, **kwargs):

        message_id = kwargs['id']
        message = Message.objects.get(id=message_id)

        # recupera o nome que o email deve ser respondido
        mail_to = message.property_set.filter(key='Return-Path').first()
        mail_to = self.__clean_mail_to(mail_to.value)

        # envia email de proposta do forum de inteligencia de mercado
        send(mail_to, 'Informacao Curso de Scrum', {}, '40bded05-3546-42c5-bc45-fa9143420ea2')

        return HttpResponse()

    def __clean_mail_to(self, mail_to):
        email = ''
        for char in mail_to:
            if char not in " <>":
                email = '%s%s' % (email, char)
        return email





