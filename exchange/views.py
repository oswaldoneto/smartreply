import email
import imaplib

from django.http.response import HttpResponse

# Create your views here.
from django.views.generic.base import View

from exchange.models import EmailServer
from mail.models import Message, Property, Payload


class FetchAllView(View):

    def get(self, request, *args, **kwargs):
        servers = EmailServer.objects.filter(active=True)
        for server in servers:
            self.__fetchall_server(server, server.mailbox_set.filter(active=True))
        return HttpResponse()

    def __fetchall_server(self, server, mailboxes):

        #conecta no servidor de email
        mail = imaplib.IMAP4_SSL(server.host)
        mail.login(server.user, server.password)

        for mailbox in mailboxes:

            # selecionar a caixa de entrada
            mail.select(mailbox.mailbox)

            # busca todos os e-mails da caixa por id
            result, data = mail.uid('search', None, 'ALL')

            # recupera a lista de ids
            ids = data[0]

            # quebra a lista de ids
            id_list = ids.split()

            for id in id_list:

                if Message.objects.filter(uuid=id).count() > 0:
                    continue

                # pega o email pelo id selecionado
                mail_result, mail_data = mail.uid('fetch', id, '(RFC822)')

                # pega o corpo do email
                raw_mail = mail_data[0][1]

                # convert raw em objeto
                email_message = email.message_from_bytes(raw_mail)

                # persist Email Message
                message = Message.objects.create(uuid=id, server=server)

                for email_item in email_message.items():

                    # persist Email Message Property
                    Property.objects.create(key=email_item[0], value=email_item[1], message=message)

                # persist Email Message Payload
                Payload.objects.create(payload=self.__get_first_text_block(email_message), message=message)


    def __get_first_text_block(self, email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload(decode=True)
        elif maintype == 'text':
            return email_message_instance.get_payload(decode=True)













