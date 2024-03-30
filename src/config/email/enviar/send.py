import smtplib
import email.message


def enviar_email(ema, assunto, template, link):
    with open(f"src/config/email/enviar/templates/{template}", "r", encoding="utf-8") as arquivo_html:
        corpo_email = arquivo_html.read()

    corpo_email = corpo_email.replace('{{ link }}', link)

    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = 'bscbreno1904@gmail.com'
    recipients = [ema]
    msg['To'] = ', '.join(recipients)

    password = "zaxqpypgchmbsfwf"

    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'], password)
    s.sendmail(msg['From'], recipients, msg.as_string().encode('utf-8'))



