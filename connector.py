
import imaplib
import email

MAIL_USER = 'poc.febracorp@gmail.com'
MAIL_PASS = 'z1on0101'


print("Iniciando conector...")

# conectar no servidor de email
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(MAIL_USER, MAIL_PASS)

# selecionar a caixa de entrada
mail.select('inbox')

# busca todos os e-mails da caixa por id
result, data = mail.uid('search', None, 'ALL')

# recupera a lista de ids
ids = data[0]

# quebra a lista de ids
id_list = ids.split()

# pega o último id da lista
latest_email_id = id_list[-1]

# pega o email pelo id selecionado
mail_result, mail_data = mail.uid('fetch', latest_email_id, '(RFC822)')

# pega o corpo do email
raw_mail = mail_data[0][1]

# convert raw em EmailMessage object
email_message = email.message_from_string(raw_mail.decode('utf-8'))

print(raw_mail)

for email_item in email_message.items():
    print(email_item)


print("Finalizando conector")


