# Strongly inspired by old code and chatgpt
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

        # Create the message
        newMessage = MIMEMultipart()
        #newMessage.set_content('Motion detected in home@', dt_string)
        newMessage['Subject'] = "A Breach has been detected in your home, check attached images & video or call local police enforcements"
        newMessage['From'] = Sender_Email
        newMessage['To'] = Reciever_Email
        #newMessage.set_content("Intruder detected:", dt_string)

        # Adds the motion detected image to attachment to be sent as mail.
        for filename in os.listdir(imagePath):
            file_path = os.path.join(imagePath, filename)
            with open(file_path, 'rb') as file:
                part = MIMEApplication(file.read(), _subtype='octet-stream')
                part.add_header('Content-Disposition', 'attachment', filename=filename)
                newMessage.attach(part)

       # Send the message
        print("PASSWORD THEN EMAIL")
        print(Password)
        print(Sender_Email)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(Sender_Email, Password)
        server.sendmail(Sender_Email, Reciever_Email, newMessage.as_string())
        server.quit()