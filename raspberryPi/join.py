#Todo send a api request containing your ip to the hub and saving the returned id

import socket
import requests

class Join:
    
    def join(self, hostIP):
        myIP = Join.getIP()
        response = requests.get(str(hostIP) +"/camera/join/"+ str(myIP))
        data = response.text
        return int(data)
        
    def getIP():
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip


