from datetime import datetime
from time import sleep
import picamera
import os
from dotenv import load_dotenv


load_dotenv()
FILE_PATH = os.getenv('FILE_PATH')
imagePath = FILE_PATH

class Camera:
    
    # Record a video
    def record(self,id):
        camera = picamera.PiCamera(resolution=(640, 480), framerate=24)
        dt_string_vid = str(id) +'__'+ datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
        # Recording path
        recordPath = imagePath + f"/{dt_string_vid}.h264"

        camera.start_preview()
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.start_recording(recordPath)
        start = datetime.now()
        while (datetime.now() - start).seconds < 5:
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.wait_recording(0.2)
        camera.stop_recording()
        camera.stop_preview()
        camera.close()
        print("FÄRDIG!")
        
    # take picture    
    def capture(self):
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.capture("test.jpg")
        camera.close()
    
        # moves images & videos from current images to archive.
    def archive(self):
        source_folder = f'/home/pi/Desktop/picture/current//'
        destination_folder = f'/home/pi/Desktop/picture/archive//'

        # fetch all files
        for file_name in os.listdir(source_folder):
            # construct full file path
            source = source_folder + file_name
            destination = destination_folder + file_name
            # move only files
            if os.path.isfile(source):
                shutil.move(source, destination)
                print('Moved:', file_name)
        
        
        
        
