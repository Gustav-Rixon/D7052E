import socket,cv2, pickle,struct
camera = True
if camera == True:
	vid = cv2.VideoCapture(0)
else:
    exit() #Should do som error handeling
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.87.255'

port = 8080
client_socket.connect((host_ip,port))

if client_socket: 
	while (vid.isOpened()):
		try:
			img, frame = vid.read()
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			client_socket.sendall(message)
			cv2.imshow(f"TO: {host_ip}",frame)
			key = cv2.waitKey(1) & 0xFF
			if key == ord("q"):
				client_socket.close()
		except:
			print('VIDEO FINISHED!')
			break

