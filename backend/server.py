#OBS THIS IS HARDCODES FOR 192.168.1.2
import socket, cv2, pickle, struct
from flask import Flask, render_template, Response

app = Flask(__name__)

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = '192.168.1.2'
print('HOST IP:',"host_ip")
port = 8080
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
clients = []
print("Listening at",socket_address)

def show_client(addr,client_socket):
	try:
		print('CLIENT {} CONNECTED!'.format(addr))
		if client_socket: # if a client socket exists
			clients.append(client_socket)
			data = b""
			payload_size = struct.calcsize("Q")
			while True:
				while len(data) < payload_size:
					packet = client_socket.recv(4*1024) # 4K
					if not packet: break
					data+=packet
				packed_msg_size = data[:payload_size]
				data = data[payload_size:]
				msg_size = struct.unpack("Q",packed_msg_size)[0]
				
				while len(data) < msg_size:
					data += client_socket.recv(4*1024)
				frame_data = data[:msg_size]
				data  = data[msg_size:]
				frame = pickle.loads(frame_data)
				_, buffer = cv2.imencode('.jpg', frame)
				frame = buffer.tobytes()
				yield (b'--frame\r\n'
                	b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
	except Exception as e:
		print(f"CLINET {addr} DISCONNECTED")
		client_socket.close()
		pass

def disconnect(addr,client_socket):
	print('CLIENT {} DISCONNECTED!'.format(addr))
	if client_socket: client_socket.close()
	pass



@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
    client_socket,addr = server_socket.accept()
    print(addr)
    print(client_socket)
    """Video streaming route."""
    return Response(show_client(addr,client_socket),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/video_feed_terminate/<string:id>/', methods=["GET"])
def video_feed_terminate(id):
    print(clients)
    print(len(clients))
    target = clients[int(id)]
    target.close()
    clients.remove(target)
    return Response("tja")               


if __name__ == '__main__':
    app.run(port=1337)

