from gpiozero import MotionSensor
from camera import camera
pir = MotionSensor(4)
#https://gpiozero.readthedocs.io/en/stable/api_input.html
class Sensor:
    
    def motion(self):
        pir.wait_for_no_motion()
        print("You moved")
        
    def stale(self):
        pir.wait_for_motion()
        
    def getvalue(self):
        return pir.value
