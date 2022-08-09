import smtplib

from email.mime.text import MIMEText

def forget_passwordmail(usermail):
    msg = MIMEText('Testing some Mailgun awesomness')
    msg['Subject'] = "Request for new password"
    msg['From']    = "omanovservices@gmail.com"
    msg['To']      = usermail

    s = smtplib.SMTP('smtp.mailgun.org', 587)

    s.login('postmaster@sandboxcf54d2ff6bf54d17974c23afc0362c04.mailgun.org', 
    'bdefad2e5906c52e4fd7841473eedbd1-835621cf-359f9039')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

