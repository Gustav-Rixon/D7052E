from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from dotenv import load_dotenv


load_dotenv()
DRIVE_ID = os.getenv('DRIVE_ID')
driveID = DRIVE_ID
FILE_PATH = os.getenv('FILE_PATH')
imagePath = FILE_PATH
class Upload:
    
    def uploader(self):
        gauth = GoogleAuth()           
        drive = GoogleDrive(gauth)  
             
        for filename in os.listdir(imagePath):
            new_path = f"{imagePath}/{filename}"
            with open(new_path, 'rb') as file:
                file_data = file.read()
                file_name = file.name
                print(f"filnamnet fan {file.name}")
        
        upload_file_list = [file_data]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': driveID}]})
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(upload_file)
            gfile.Upload() # Upload the file  