from datetime import datetime
from time import sleep

import picamera


class Camera:
    #TODO FIX so that recording time is dependant on sensor input not just activation
    # Record a video
    def record(self):
        camera = picamera.PiCamera(resolution=(640, 480), framerate=24)
        # dd/mm/YY H:M:S TODO method for this line?
        dt_string_vid = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
        # Recording path
        recordPath = f"/home/edison/Videos/security/{dt_string_vid}.h264"

        camera.start_preview()
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.start_recording(recordPath)
        start = datetime.now()
        while (datetime.now() - start).seconds < 5:
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.wait_recording(0.2)
        camera.stop_recording()
                
        
        
        
        