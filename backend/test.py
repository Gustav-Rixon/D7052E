import http.server
import xmlrpc.client
import urllib.parse

class TestAPI(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse the POST data
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        
        # Parse the argument from the POST data
        params = urllib.parse.parse_qs(data)
        argument = params.get("argument", [None])[0]
        
        # Call the run_test method on the RPC server
        client = xmlrpc.client.ServerProxy("http://localhost:8000/", allow_none=True)
        response = client.run_test(argument)
        
        # Send the response back to the client
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response.encode())

server = http.server.HTTPServer(("localhost", 8080), TestAPI)
server.serve_forever()