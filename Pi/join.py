#Todo send a api request containing your ip to the hub and saving the returned id

import socket


def getIP(self):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


