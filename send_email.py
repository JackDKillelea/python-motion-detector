import smtplib
import imghdr
from email.message import EmailMessage
import variables

def email(image_path, encoding):
    print("Sending email...")
    email_message = EmailMessage()
    email_message["Subject"] = "Image Analysis Report"
    email_message["From"] = variables.get_receiver()
    email_message["To"] = variables.get_receiver()
    email_message.set_content(f"Image analysis report has been generated."
                              f"\n\nPlease find the attached report in the provided image path: {image_path}")

    with open(image_path, "rb") as image:
        content = image.read()

    email_message.add_attachment(content, filename="report.png", maintype="application",
                                 subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.starttls()
    gmail.ehlo()
    gmail.login(variables.get_username(), variables.get_password())
    gmail.sendmail(variables.get_username(), variables.get_receiver(), email_message.as_string())

