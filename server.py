import http.server
import socketserver
import urllib.parse
import os

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

        # If download parameter is present or if it's a PDF download request
        if path.endswith('.pdf'):
            file_path = os.path.join(DIRECTORY, path.lstrip('/'))
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                # If requested with ?download=1 or ?dl=1, force download attachment
                if 'download' in query or 'dl' in query or not 'view' in query:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/pdf')
                    self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                    self.send_header('Content-Length', str(os.path.getsize(file_path)))
                    self.end_headers()
                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                    return
        
        super().do_GET()

print(f"Starting DEC Study & PDF Download Server on 0.0.0.0:{PORT}...")
with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
    httpd.allow_reuse_address = True
    print(f"Server active at http://0.0.0.0:{PORT}")
    httpd.serve_forever()
