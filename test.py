__author__ = 'DanielAjisafe'
import EnergyProject.database.database_connect as dc
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
#
# email = "noreply.energysaver@gmail.com"
# to = "oluwatoyinaij@gmail.com"
#
#
# msg = MIMEMultipart()
# msg['From'] = email
# msg['To'] = to
# msg['Subject'] = "Energy Saver"
# body = "Test"
# msg.attach(MIMEText(body, 'plain'))
#
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login(email, "energys@ver")
# server.login(email, "YOUR PASSWORD")
# text = msg.as_string()
# server.sendmail(email, to, text)
# server.quit()

msg = 'fod'
try:
    raise ValueError(msg)
except ValueError as e:
    if str(e) is msg:
        print('works')