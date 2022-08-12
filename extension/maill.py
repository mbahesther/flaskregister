import os
import smtplib

from email.mime.text import MIMEText

def send_mail(usermail):
    msg = MIMEText('Testing some Mailgun awesomness')
    msg['Subject'] = "Thank for registering"
    msg['From']    = "omanovservices@gmail.com"
    msg['To']      = usermail

    s = smtplib.SMTP('smtp.mailgun.org', 587)

    s.login(os.getenv('MY_DOMAIN_NAME'), os.getenv('SMTP_PASSWORD'))
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

