from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from dotenv import load_dotenv


load_dotenv()
DRIVE_ID = os.getenv('DRIVE_ID')
driveID = DRIVE_ID
class Upload:
    
    def uploader(self, movie, pic):
        gauth = GoogleAuth()           
        drive = GoogleDrive(gauth)

        upload_file_list = [movie]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': driveID}]})
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(upload_file)
            gfile.Upload() # Upload the file  