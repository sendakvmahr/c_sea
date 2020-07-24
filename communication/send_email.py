import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

def _login():
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls()                            #enable security
    session.login(config.gmail_username, config.gmail_password)    #login with mail_id and password
    return session

def send_email(body, subject="Update From Cerulean Sea", recipients=[config.gmail_username], attachments=[]):
    session = _login()
    message = MIMEMultipart()
    message['From'] = config.gmail_username
    message['To'] = ", ".join(recipients)
    message['Subject'] = subject  #The subject line
    message.attach(MIMEText(body, 'plain'))
    for file in attachments:
        with open(file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            name = file.split("\\")[-1]
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {name}",
            )
            message.attach(part)
    email = message.as_string()
    session.sendmail(config.gmail_username,config.gmail_username, email)

