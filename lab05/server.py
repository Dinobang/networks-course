import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(sender, receiver, subject, msg, msg_type='plain', img_path=None):

    msg_obj = MIMEMultipart()

    msg_obj['From'] = sender
    msg_obj['To'] = receiver
    msg_obj['Subject'] = subject
    
    if msg_type == 'plain':
        msg_obj.attach(MIMEText(msg, 'plain'))
    elif msg_type == 'html':
        msg_obj.attach(MIMEText(msg, 'html'))

    if img_path:
        with open(img_path, "rb") as img_file:
            img_part = MIMEBase('application', 'octet-stream')
            img_part.set_payload(img_file.read())
            encoders.encode_base64(img_part) 
            msg_obj.attach(img_part)


    server = 'smtp.gmail.com'
    port = 587
    username = 'mozgolinan@gmail.com'  
    password = 'zimy hxqf mfis retd'     

    try:
        server = smtplib.SMTP(server, port)
        server.starttls() 
        server.login(username, password)
        server.sendmail(sender, receiver, msg_obj.as_string())
        server.quit()
        print(f"Email sent!!!!!!!! to {receiver}")
    except Exception as e:
        print(f"Failed to send email((((: {e}")     


def main():
    sender = 'mozgolinan@gmail.com' 
    receiver = 'mozgolinan@gmail.com'
    subject = 'HOMEWORK'
    msg_type = 'plain'

    msg = 'Hello, how are you? I want to die with this homework, u know?'

    img_path = '/Users/pusya/Desktop/lab03/files/dog.jpeg'
    send_email(sender, receiver, subject, msg, msg_type, img_path)

if __name__ == "__main__":
    main() 