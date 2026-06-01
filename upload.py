import http.server
import socketserver
import cgi
import os
import json
import shutil

UPLOAD_DIR = '/tmp/uploads'

if os.path.exists(UPLOAD_DIR):
    shutil.rmtree(UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         }
            )
            fileitem = form['file']
            if fileitem.filename:
                # Get the absolute path inside the container workspace
                filename = os.path.basename(fileitem.filename)
                filepath = os.path.join(UPLOAD_DIR, filename)
                with open(filepath, 'wb') as f:
                    f.write(fileitem.file.read())
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'path': filepath}).encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "No file uploaded"}')
        elif self.path == '/import_backup':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         }
            )
            fileitem = form['file']
            if fileitem.filename:
                import subprocess
                filepath = "/tmp/import_backup.tar.gz"
                with open(filepath, 'wb') as f:
                    f.write(fileitem.file.read())
                
                # Extract to root preserving directory structure (root/.gemini and data/)
                result = subprocess.run(["tar", "-xzf", filepath, "-C", "/"], capture_output=True)
                if result.returncode == 0:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "success"}')
                else:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': result.stderr.decode()}).encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "No file uploaded"}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        import subprocess
        
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/kill':
            query = parse_qs(parsed_path.query)
            session_id = query.get('session_id', [None])[0]
            if session_id and session_id.isdigit():
                socket_file = f"/tmp/agy_{session_id}.socket"
                log_file = f"/data/session_{session_id}.log"
                # Kill processes attached to the socket and remove files
                subprocess.run(["fuser", "-k", socket_file], capture_output=True)
                if os.path.exists(socket_file):
                    try: os.remove(socket_file)
                    except: pass
                if os.path.exists(log_file):
                    try: os.remove(log_file)
                    except: pass
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "killed"}')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid session_id"}')
        elif parsed_path.path == '/version_check':
            import subprocess, urllib.request, json
            try:
                current = subprocess.check_output(['/usr/local/bin/agy', '--version'], stderr=subprocess.STDOUT).decode().strip()
            except:
                current = "unknown"
            
            try:
                req = urllib.request.Request('https://antigravity.google/cli/version.txt')
                with urllib.request.urlopen(req, timeout=3) as response:
                    latest = response.read().decode('utf-8').strip()
            except:
                latest = current # If it fails, assume up to date
                
            update_available = (latest != current and latest != "" and current != "unknown")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'update_available': update_available,
                'current': current,
                'latest': latest
            }).encode())
            
        elif parsed_path.path == '/update_cli':
            import subprocess
            try:
                # Run the update script
                subprocess.run(['bash', '-c', 'curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- -d /usr/local/bin'], check=True)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'{"status": "error"}')
        elif parsed_path.path == '/export_backup':
            import subprocess, os
            backup_file = "/tmp/antigravity_backup.tar.gz"
            if os.path.exists(backup_file):
                os.remove(backup_file)
            
            targets = []
            if os.path.exists("/root/.gemini"): targets.append("root/.gemini")
            if os.path.exists("/data"): targets.append("data")
            if os.path.exists("/config/.gemini"): targets.append("config/.gemini")
            
            if targets:
                # Create tar archive
                subprocess.run(["tar", "-czf", backup_file, "-C", "/"] + targets, capture_output=True)
                
                with open(backup_file, "rb") as f:
                    file_data = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/gzip')
                self.send_header('Content-Disposition', 'attachment; filename="antigravity_backup.tar.gz"')
                self.send_header('Content-Length', str(len(file_data)))
                self.end_headers()
                self.wfile.write(file_data)
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Nothing to backup"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    PORT = 8097
    print(f"Starting upload server on port {PORT}")
    with socketserver.TCPServer(("", PORT), UploadHandler) as httpd:
        httpd.serve_forever()
