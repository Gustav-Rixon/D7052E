import os
import time
import camera
import mail
import threading
import sensor
import upload
import join
import delete



HUB_IP = os.getenv('HUB_IP')
HubIP = HUB_IP
class Main:

    def __init__(self):
        # Sensor client
        self.sensor_main = sensor.Sensor()
        # Camera client
        self.camera_main = camera.Camera()
        # Email client
        self.mail_main = mail.Email()
        #upload to drive client
        self.upload_main = upload.Upload()
        # Join client
        self.join_main = join.Join()
        # Delete client
        self.delete_main = delete.Delete()
    
    def start(self):
        print("starting...")
        id = self.join_main.join(HubIP)
        print(id)
        while True:
            capture_camera_thread = threading.Thread(target=self.camera_main.capture, args=(id, ))
            record_camera_thread = threading.Thread(target=self.camera_main.record, args=(id, ))
            mail_thread = threading.Thread(target=self.mail_main.alert, args=())
            upload_thread = threading.Thread(target=self.upload_main.uploader, args=())
            if(self.sensor_main.getvalue() == 0):
                self.sensor_main.stale()
            elif(self.sensor_main.getvalue() == 1):
                #self.camera_main.record()
                print(f"Taking picture")
                capture_camera_thread.start()
                capture_camera_thread.join()
                print(f"recording...")
                record_camera_thread.start()
                record_camera_thread.join()
                print(f'sending email...')
                mail_thread.start()
                print(f"uploading")
                upload_thread.start()
                # Check status if home or not
                mail_thread.join(timeout=4)
                upload_thread.join(timeout=4)
                self.sensor_main.motion()
                self.delete_main.clear()

if __name__ == "__main__":
    main = Main()
    main.start()
