import smtplib
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from application import app
from flask import render_template


def send_async_email(app, server, msg, sender, recipients):
    with app.app_context():
        server.send_message(msg, sender, recipients)
        server.quit()


def send_email(sender, recipients, subject, text_body, html_body):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipients
    msg['Subject'] = subject
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))
    server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    server.ehlo()
    server.starttls()
    server.login(sender, app.config['MAIL_PASSWORD'])
    Thread(target=send_async_email, args=(app, server, msg, sender, recipients)).start()
    #server.send_message(msg, sender, recipients)
    # server.quit()


def send_password_reset_mail(user):
    token = user.get_reset_password_token()
    send_email(sender=app.config['MAIL_USERNAME'], recipients=user.email, subject="ChatBox password reset", text_body=render_template(
        'email//reset_password.txt', user=user, token=token), html_body=render_template('email/reset_password.html', user=user, token=token))
