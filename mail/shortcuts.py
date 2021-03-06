import ssl
import os
import sendgrid
from sendgrid.helpers.mail.mail import Mail, Personalization, Email, Content, Substitution


ENV_SENDGRID_KEY = 'SENDGRID_API_KEY'

FROM = 'poc.febracorp@gmail.com'
BCCS = []


def send(mail_to, subject, substitution, template_id):

    def prepare_data():

        mail = Mail()

        mail.set_from(Email(FROM))

        mail.set_subject(subject)

        mail.set_template_id(template_id)

        personalization = Personalization()

        personalization.add_to(Email(mail_to))

        mails_bcc = BCCS
        for mail_bcc in BCCS:
            if mail_bcc not in mails_bcc:
                personalization.add_bcc(Email(mail_bcc))

        for key in substitution:
            personalization.add_substitution(Substitution(key, substitution[key]))

        mail.add_personalization(personalization)

        mail.add_content(Content("text/plain", "some text here"))
        mail.add_content(Content("text/html", "<html><body>some text here</body></html>"))

        return mail.get()

    sendgrid_key = os.environ[ENV_SENDGRID_KEY]

    try:

        ###
        ### ---------------------------------------------------------------
        ### Workaround for SSL INVALID CERTIFICATE ON PYTHON 3.6 + MAC OS X
        ###
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        ###
        ### Workaround for SSL INVALID CERTIFICATE ON PYTHON 3.6 + MAC OS X
        ### ---------------------------------------------------------------
        ###

        sg = sendgrid.SendGridAPIClient(apikey=sendgrid_key)

        # prepare api send request data
        data = prepare_data()

        # api send call
        response = sg.client.mail.send.post(request_body=data)

        print(response)

    except Exception as e:
        raise e