import time
import camera
import mail
import threading
import sensor
import upload
import join

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
    
    def start(self):
        print("starting...")
        while True:
            record_camera_thread = threading.Thread(target=self.camera_main.record, args=())
            mail_thread = threading.Thread(target=self.mail_main.alert, args=())
            upload_thread = threading.Thread(target=self.mail_main.alert, args=())
            if(self.sensor_main.getvalue() == 0):
                self.sensor_main.stale()
            elif(self.sensor_main.getvalue() == 1):
                #self.camera_main.record()
                print(f"recording...")
                record_camera_thread.start()
                record_camera_thread.join()
                print(f'sending email...')
                mail_thread.start()
                print(f"uploading")
                upload_thread.start()
                # Check status if home or not
                mail_thread.join()
                upload_thread.join()
                self.sensor_main.motion()
                #camera_main.archive()
                
"""""
            # Printing that the system is on and checking
            print("Checking security...")
            time.sleep(1)
            # Get motion sensor id last breached in secconds (s)
            breached_time = fibaro_main.get_last_breached()
            print(f'breached_time = {breached_time}')
            hue_thread = threading.Thread(
                target=self.hue_main.alarm_environment, args=())
            capture_camera_thread = threading.Thread(
                target=self.camera_main.capture, args=())
            record_camera_thread = threading.Thread(
                target=self.camera_main.record, args=())
            mail_thread = threading.Thread(target=self.mail_main.alert, args=())
            # Check status if home or not
            is_home = self.mail_main.check()

            # If fib sensor was breached in the last 10 secconds and not home activate alarm.
            print(is_home)
            print(f'breached_time = {breached_time}')

            if breached_time < 20 and not is_home:
                print(f'activating alarm...')
                hue_thread.start()
                print(f'taking screenshoot...')
                capture_camera_thread.start()
                capture_camera_thread.join()
                print(f'recording...')
                record_camera_thread.start()
                record_camera_thread.join()
                print(f'sending email...')
                mail_thread.start()
                # Assure remaining threads have finished execution.
                hue_thread.join()
                mail_thread.join()
                camera_main.archive()

"""

if __name__ == "__main__":
    main = Main()
    main.start()
