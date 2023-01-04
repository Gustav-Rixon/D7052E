# Imports
import code
import email
import imaplib
import imghdr
import os
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from email.message import EmailMessage


load_dotenv()

EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
FILE_PATH = os.getenv('FILE_PATH')
#add your mail adress
Sender_Email = EMAIL_USERNAME
Reciever_Email = EMAIL_USERNAME
Password = EMAIL_PASSWORD

# Raspberry Pi
imagePath = FILE_PATH


class Email:

    # sends alert messages with images and videos to the gmail.
    def alert(self):
        # datetime object containing current date and time
        #now = datetime.now()
        # Date YY-mm-dd time: H:M:S
        dt_string = datetime.now().strftime(
            " date: " + "%Y-%m-%d" + " time: " + "%H:%M:%S")

        # Email message
        newMessage = EmailMessage()
        newMessage.set_content('Motion detected in home@', dt_string)
        newMessage['Subject'] = "A Breach has been detected in your home, check attached images & video or call local police enforcements"
        newMessage['From'] = Sender_Email
        newMessage['To'] = Reciever_Email
        newMessage.set_content("Intruder detected:", dt_string)

        # Adds the motion detected image to attachment to be sent as mail.
        for filename in os.listdir(imagePath):
            new_path = f"{imagePath}/{filename}"
            with open(new_path, 'rb') as file:
                file_data = file.read()
                file_name = file.name
                print(f"filnamnet fan {file.name}")
                newMessage.add_attachment(
                    file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # Sending the mail using the SMTP gmail.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(Sender_Email, Password)
            smtp.send_message(newMessage)

    # Check gmail for Out/Home gmail to set boolean value.
    
    ##TODO GAMMAL KOD GÅR INTE ATT ANVÄNDA SEN 30MAY 2022
    def check(self):

        # https://www.systoolsgroup.com/imap/
        gmail_host = 'imap.gmail.com'

        # set connection
        mail = imaplib.IMAP4_SSL(gmail_host)

        # login
        mail.login(Sender_Email, Password)

        # select inbox
        mail.select("INBOX")

        # select specific mails
        _, selected_mails = mail.search(None, '(FROM ' + Sender_Email + ')')

        # Loop through mails, if subject Home / Out found return is_home else return is is_home.
        for num in reversed(selected_mails[0].split()):
            typ, data = mail.fetch(
                num, '(RFC822.SIZE BODY[HEADER.FIELDS (SUBJECT)])')
            email_message = email.message_from_bytes(data[0][1])

        # access data
            if (email_message["subject"] == "Home"):
                print("Home")
                return True

            if (email_message["subject"] == "Out"):
                print("Out")
                return False

        return False