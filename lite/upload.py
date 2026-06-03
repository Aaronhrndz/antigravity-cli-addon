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
                    import shutil
                    shutil.copyfileobj(fileitem.file, f)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'path': filepath}).encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "No file uploaded"}')
        elif self.path.startswith('/import_chunk'):
            from urllib.parse import urlparse, parse_qs
            parsed_path = urlparse(self.path)
            query = parse_qs(parsed_path.query)
            chunk_index = int(query.get('chunk_index', ['0'])[0])
            total_chunks = int(query.get('total_chunks', ['1'])[0])
            
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
                mode = 'wb' if chunk_index == 0 else 'ab'
                with open(filepath, mode) as f:
                    import shutil
                    shutil.copyfileobj(fileitem.file, f)
                
                if chunk_index == total_chunks - 1:
                    # Extract to root preserving directory structure
                    result = subprocess.run(["tar", "-xzf", filepath, "-C", "/"], capture_output=True)
                    if result.returncode == 0:
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"status": "success"}')
                        
                        # Auto-restart the Add-on via Supervisor API after 2 seconds
                        import os
                        token = os.environ.get("SUPERVISOR_TOKEN")
                        if token:
                            subprocess.Popen(["bash", "-c", f"sleep 2 && curl -s -X POST -H 'Authorization: Bearer {token}' http://supervisor/addons/self/restart"])
                    else:
                        self.send_response(500)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': result.stderr.decode()}).encode())
                else:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "chunk_received"}')
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
            if os.path.exists("/data/.gemini"): targets.append("data/.gemini")
            if os.path.exists("/config/.gemini"): targets.append("config/.gemini")
            
            if targets:
                self.send_response(200)
                self.send_header('Content-Type', 'application/gzip')
                self.send_header('Content-Disposition', 'attachment; filename="antigravity_backup.tar.gz"')
                self.end_headers()
                
                # Stream tar directly to the network to prevent disk/RAM exhaustion
                import subprocess
                proc = subprocess.Popen(["tar", "-czf", "-", "-C", "/"] + targets, stdout=subprocess.PIPE)
                import shutil
                shutil.copyfileobj(proc.stdout, self.wfile)
                proc.stdout.close()
                proc.wait()
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Nothing to backup"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    PORT = 62897
    print(f"Starting upload server on port {PORT}")
    with socketserver.TCPServer(("", PORT), UploadHandler) as httpd:
        httpd.serve_forever()
