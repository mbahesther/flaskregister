from distutils.ccompiler import gen_lib_options

import os
import smtplib
from flask import url_for
from lets import my_cursor, mydb,MySQLdb

import math, random

# function to generate OTP
def generateOTP() :
	digits = "0123456789"
	OTP = ""


	for i in range(4) :
		OTP += digits[math.floor(random.random() * 10)]

	return OTP





from email.mime.text import MIMEText
def forget_passwordmail(user):
    otp = generateOTP()
   
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
   # my_cursor.execute('INSERT INTO user_register(otp) VALUES', [otp])
    my_cursor.execute(f' UPDATE `user_register` SET `otp`={otp} WHERE `email`= [{user}]' )
    # my_cursor.execute(f' UPDATE `user_register` SET `otp`=[{otp}]  WHERE `email`= [{user}]' )
    user = my_cursor.fetchone()

    msg = MIMEText(f''' We received your request for a single-use code to use.
    Your single-use code is: {otp}
    If you did not make this request simply ignore''' )
    msg['Subject'] = "Request for new password"
    msg['From']    = "omanovservices@gmail.com"
    msg['To']      = user

    s = smtplib.SMTP('smtp.mailgun.org', 587)

    s.login(os.getenv('MY_DOMAIN_NAME'), os.getenv('SMTP_PASSWORD'))
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

