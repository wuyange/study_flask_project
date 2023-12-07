from app.exts import mail
from flask_mail import Message

def send_verification_code(sender, code):
    message = Message(subject='python论坛的注册码',
                      recipients=[sender],
                      body=f'验证码为:{code}')
    mail.send(message)


