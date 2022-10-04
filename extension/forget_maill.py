from lets import app
import os
import ssl
import smtplib
from flask import url_for
from email.message import EmailMessage


from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user




jwt_manager = JWTManager(app)

def forget(usermail):
        email_sender = 'omanovservices@gmail.com'
        email_password = os.getenv('EMAIL_PASSWORD')

        email_receiver = usermail
        subject = "Password reset"
        access_token = create_access_token(identity=usermail)

        body =  url_for('passwordreset', token=access_token, _external=True) 
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())



# from mailjet_rest import Client
# import os
# api_key = os.getenv('API_KEY ')
# api_secret = os.getenv('API_SECRET_KEY')
# mailjet = Client(auth=(api_key, api_secret), version='v3.1')


# def forget_passwordmail(useremail):
   
#     access_token = create_access_token(identity=useremail)
   
#     data = {
#     'Messages': [
#         {
#         "From": {
#             "Email": "omanovservices@gmail.com",
#             "Name": "oma's Empire"
#         },
#         "To": [
#             {
#             "Email": useremail,
#             "Name": "oma"
#             }
#         ],
#         "Subject": "Request for new password",
#         "TextPart": "Password Reset!!!",
#         "HTMLPart": (url_for('passwordreset', token=access_token, _external=True)) ,
#         "CustomID": "AppGettingStartedTest"
#         }
#     ]
#     }
#     result = mailjet.send.create(data=data)
#     print(result.status_code)
#     print(result.json())



#MAILGUN
# import smtplib
# from lets import my_cursor, mydb,MySQLdb

# from email.mime.text import MIMEText
# def forget_passwordmail(user):
#     otp = generateOTP()
   
#     my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
#    # my_cursor.execute('INSERT INTO user_register(otp) VALUES', [otp])
#     my_cursor.execute(f' UPDATE `user_register` SET `otp`={otp} WHERE `email`= [{user}]' )
#     # my_cursor.execute(f' UPDATE `user_register` SET `otp`=[{otp}]  WHERE `email`= [{user}]' )
#     user = my_cursor.fetchone()

#     msg = MIMEText(f''' We received your request for a single-use code to use.
#     Your single-use code is: {otp}
#     If you did not make this request simply ignore''' )
#     msg['Subject'] = "Request for new password"
#     msg['From']    = "omanovservices@gmail.com"
#     msg['To']      = user

#     s = smtplib.SMTP('smtp.mailgun.org', 587)

#     s.login(os.getenv('MY_DOMAIN_NAME'), os.getenv('SMTP_PASSWORD'))
#     s.sendmail(msg['From'], msg['To'], msg.as_string())
#     s.quit()

