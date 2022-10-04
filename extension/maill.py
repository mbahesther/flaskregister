from mailjet_rest import Client
import os
api_key = 'c19a631f79ee42c7d3785f6fd9fad490'
api_secret = 'f1a0e119fec4096ae2a906fce7daa6e0'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def send_mail(useremail):
    data = {
    'Messages': [
        {
        "From": {
            "Email": "omanovservices@gmail.com",
            "Name": "oma's Empire"
        },
        "To": [
            {
            "Email": useremail,
            "Name": "oma"
            }
        ],
        "Subject": "Thanks for Registering",
        "TextPart": "Thanks for registering!!!",
        "HTMLPart": "<h3>Welcome on board to oma's empire <a href='#'></a>!</h3><br />Thanks for registering lets have a great time with you on our app",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())


#mailgun
# import os
# import smtplib

# from email.mime.text import MIMEText

# def send_mail(usermail):
#     msg = MIMEText('Testing some Mailgun awesomness')
#     msg['Subject'] = "Thank for registering"
#     msg['From']    = "omanovservices@gmail.com"
#     msg['To']      = usermail

#     s = smtplib.SMTP('smtp.mailgun.org', 587)

#     s.login(os.getenv('MY_DOMAIN_NAME'), os.getenv('SMTP_PASSWORD'))
#     s.sendmail(msg['From'], msg['To'], msg.as_string())
#     s.quit()

