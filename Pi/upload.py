from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from dotenv import load_dotenv


load_dotenv()
# ID of the destination folder
DRIVE_ID = os.getenv('DRIVE_ID')
driveID = DRIVE_ID
FILE_PATH = os.getenv('FILE_PATH')
imagePath = FILE_PATH
class Upload:
    
    def uploader(self):
        # Load the client secrets from the "client_secrets.json" file
        gauth = GoogleAuth()
        gauth.LoadClientConfigFile("client_secrets.json")

        # Try to load the saved credentials
        gauth.LoadCredentialsFile("credentials.json")

        # If the credentials are invalid or missing, run the OAuth2 flow
        if gauth.credentials is None or gauth.access_token_expired:
            gauth.Refresh()

        # Save the credentials for the next run
        gauth.SaveCredentialsFile("credentials.json")

        # Create a service object
        drive = GoogleDrive(gauth)
                # Get a list of all files in the folder
        filenames = os.listdir(imagePath)  
             
        # Upload each file
        for filename in filenames:
            file_path = os.path.join(imagePath, filename)
            file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": driveID}]})
            file.SetContentFile(file_path)
            file.Upload()
            print(F'File ID: {file["id"]}') 
            