import http.server
import socketserver
import urllib.parse
import os
import socket

PORT = 8080
DIRECTORY = "/home/user/DEC"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable CORS for preview environment
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Handle PDF download requests
        if path.endswith('.pdf'):
            file_path = os.path.join(DIRECTORY, path.lstrip('/'))
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                # If requested without view=1, send attachment headers for direct download
                if 'view' not in query:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/pdf')
                    self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                    self.send_header('Content-Length', str(os.path.getsize(file_path)))
                    self.end_headers()
                    try:
                        with open(file_path, 'rb') as f:
                            while chunk := f.read(65536):
                                self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        pass
                    return
        
        super().do_GET()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except (AttributeError, OSError):
            pass
        super().server_bind()

if __name__ == '__main__':
    print(f"Starting DEC Study & PDF Download Server on 0.0.0.0:{PORT}...")
    with ReusableTCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
        print(f"Server active at http://0.0.0.0:{PORT}")
        httpd.serve_forever()
