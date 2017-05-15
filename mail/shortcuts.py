import ssl
import os
import sendgrid
from sendgrid.helpers.mail.mail import Mail, Personalization, Email, Content


def send():

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


    def prepare_data(template_id, mail_to):

        mail = Mail()

        mail.set_from(Email('poc.febracorp@gmail.com'))

        mail.set_subject('Titulo vai aqui')

        mail.set_template_id(template_id)

        personalization = Personalization()

        mails_bcc = ['oswaldo.neto@gmail.com', ]
        for mail_bcc in mails_bcc:
            if mail_bcc not in mails_bcc:
                personalization.add_bcc(Email(mail_bcc))

        personalization.add_to(Email(mail_to))

        mail.add_personalization(personalization)

        mail.add_content(Content("text/html", " "))

        return mail.get()

    #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
    sendgrid_key = os.environ['SENDGRID_API_KEY']


    try:
        sg = sendgrid.SendGridAPIClient(apikey=sendgrid_key)

        # prepare api send request data
        data = prepare_data('2a1e1443-9a14-4560-be2a-c3a41fd01b21', 'oswaldo.neto@gmail.com')

        # api send call
        response = sg.client.mail.send.post(request_body=data)

        print(response)

    except Exception as e:
        raise e