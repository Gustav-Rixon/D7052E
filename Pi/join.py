#Todo send a api request containing your ip to the hub and saving the returned id

import socket
import requests

class Join:
    
    def join(hostIP):
        myIP = Join.getIP()
        abc = requests.get(hostIP +"/camera/join/"+ myIP)
        return int(abc)
        
    def getIP():
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip


