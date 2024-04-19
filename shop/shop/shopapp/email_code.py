import smtplib
from email.mime.text import MIMEText


def send_email(message, receiver):
    sender = "pet30207@gmail.com"
    password = "fpdjslfiwzkttyau"
    receiver = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "Код подтверждения."
        server.sendmail(sender, receiver, msg.as_string())
        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"
