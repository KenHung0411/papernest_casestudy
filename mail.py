import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

class EmailService:

    subject = "clients phone call report"
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls

    def __init__(self, sender_email, passwd, receiver_email,  client_list):
        self.sender_email = sender_email
        self.passwd = passwd
        self.receiver_email = receiver_email
        self.body =  "\n".join(client_list)

    def mail_body(self):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = self.subject
        message["Bcc"] = self.receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(self.body, "plain"))

        # Open csv file in binary mode
        with open("./output/result.csv", "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            "attachment; filename= result.csv",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        return text
  

    def send_mail(self):
        text = self.mail_body()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.passwd)
            server.sendmail(self.sender_email, self.receiver_email, text)



if __name__ == "__main__":
    sender_email = os.environ["MAIL_SENDER"]
    passwd = os.environ["MAIL_PWD"]
    receiver_email = "ken.hung.me@gmail.com"
    client_list = ["Ken Hung", "Alexandra Gajdos", "John Legend", "Carl Hu"]
    mail_service = EmailService(sender_email, passwd, receiver_email, client_list)
    mail_service.send_mail()