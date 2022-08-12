import os
import smtplib
from flask import url_for


from email.mime.text import MIMEText
def forget_passwordmail(user):
    token= user.get_reset_token()
    msg = MIMEText(f'''To reset your password click on the following 
    link:{url_for('reset_token', token=token, _external=True)} 
    If you did not make this request simply ignore''')
    msg['Subject'] = "Request for new password"
    msg['From']    = "omanovservices@gmail.com"
    msg['To']      = user.email

    s = smtplib.SMTP('smtp.mailgun.org', 587)

    s.login(os.getenv('MY_DOMAIN_NAME'), os.getenv('SMTP_PASSWORD'))
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

