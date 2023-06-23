import smtplib
from email.mime import multipart
from email.mime import text
import email

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "soumyag27402@gmail.com"
SENDER_PASSWORD = ""


def send_email(to_address, subject, message, att=None):
    msg = multipart.MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(text.MIMEText(message, "html"))
    if att is not None:
        with open(att, "rb") as attach:
            stream = email.mime.base.MIMEBase("application", "octet-stream")
            stream.set_payload(attach.read())
        email.encoders.encode_base64(stream)
        stream.add_header("Content-Disposition", f"attachment;filename={att}")
        msg.attach(stream)
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
