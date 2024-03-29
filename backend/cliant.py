import socket,cv2, pickle,struct
import xmlrpc.server

class TestRPC:
	def run_test(self, argument):
		camera = True
		if camera == True:
			vid = cv2.VideoCapture(0)
		else:
			exit() #Should do som error handeling
   
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		host_ip = '192.168.1.2'

		port = 8080
		client_socket.connect((host_ip,port))

		if client_socket: 
			while (vid.isOpened()):
				try:
					img, frame = vid.read()
					a = pickle.dumps(frame)
					message = struct.pack("Q",len(a))+a
					client_socket.sendall(message)
					#cv2.imshow(f"TO: {host_ip}",frame)
				except:
					client_socket.close()
					print('VIDEO FINISHED!')
					break
		pass

server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
server.register_instance(TestRPC())

# Run the RPC server
server.serve_forever()
