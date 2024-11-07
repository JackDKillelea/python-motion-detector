import smtplib, ssl
import variables

def email(message, encoding):
    host = "smtp.gmail.com"
    port = 465

    username = variables.get_username()
    password = variables.get_password()
    receiver = variables.get_receiver()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message.encode(encoding))