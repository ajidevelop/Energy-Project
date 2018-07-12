__author__ = 'DanielAjisafe'
import re
import smtplib
import secrets
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def verify_email(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match is None:
        raise ValueError


def send_verification_email(e):
    email = "noreply.energysaver@gmail.com"
    token = generate_token()
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = e
    msg['Subject'] = "Energy Saver Verification Email"
    body = f"Here's your verification code:\n{token}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, "energys@ver")
    text = msg.as_string()
    server.sendmail(email, e, text)
    server.quit()

    return token


def generate_token():
    return secrets.token_urlsafe(20)



