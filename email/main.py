from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = ' 2525'
app.config['MAIL_USERNAME'] = 'b24581b0420b91'
app.config['MAIL_PASSWORD'] = '27606a858eb5a0'
app.config['MAIL_USE_TLS'] = 'True'
app.config['MAIL_USE_SSL'] = 'False'
mail = Mail(app)

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        msg = Message("hey", sender='noreply@demo.com', recipients=[''])
        msg.body = "hey how are you doing"
        mail.send(msg)
        return "sent mail"
    return render_template('index.html')


#s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#from itsdangerous import URLSafeTimedSerializer


if __name__ == '__main__':
 app.run(debug=True)