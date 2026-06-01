#!/usr/bin/env python3
import os
import sys
import time
import json
import re
import threading
import pexpect
import urllib.request
import urllib.parse

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
API_URL = f"https://api.telegram.org/bot{TOKEN}"
UPLOAD_DIR = "/tmp/uploads"

if not TOKEN or not CHAT_ID:
    print("Telegram bot token or chat ID not provided. Exiting.")
    sys.exit(0)

# We use pexpect to attach to the dtach socket
child = None

def clean_text(text):
    # Remove standard ANSI escape sequences
    text = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)
    
    # Process \r (carriage return) and \b (backspace) to emulate basic terminal behavior
    final_lines = []
    for line in text.split('\n'):
        # Carriage return overwrites the line
        parts = line.split('\r')
        line = parts[-1]
        
        # Backspace removes previous character
        while '\b' in line:
            new_line = re.sub(r'[^\b]\b', '', line)
            if new_line == line:
                # If nothing changed, just strip leading \b
                line = line.lstrip('\b')
                break
            line = new_line
            
        line = line.strip()
        if line and line not in ['?', '>']:
            final_lines.append(line)
            
    return '\n'.join(final_lines)

def send_message(text, parse_mode=None):
    url = f"{API_URL}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    if parse_mode:
        data["parse_mode"] = parse_mode
        
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error sending message: {e}")

def send_typing_action():
    url = f"{API_URL}/sendChatAction"
    data = {
        "chat_id": CHAT_ID,
        "action": "typing"
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error sending chat action: {e}")

def get_file_url(file_id):
    url = f"{API_URL}/getFile?file_id={file_id}"
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())
        if data.get("ok"):
            file_path = data["result"]["file_path"]
            return f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    except Exception as e:
        print(f"Error getting file url: {e}")
    return None

def download_file(url, dest_path):
    try:
        urllib.request.urlretrieve(url, dest_path)
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

def pexpect_thread():
    global child
    # Telegram gets its own dedicated and isolated CLI session
    child = pexpect.spawn('/usr/local/bin/agy', env={"NO_COLOR": "1", "TERM": "dumb", **os.environ}, encoding='utf-8', dimensions=(50, 100))
    
    buffer = ""
    last_typing_time = 0
    
    while True:
        try:
            # Read in chunks, waiting up to 1.0s for more data to prevent fragmented messages
            chunk = child.read_nonblocking(size=4096, timeout=1.0)
            buffer += chunk
            
            current_time = time.time()
            if len(buffer) > 0 and current_time - last_typing_time > 3:
                send_typing_action()
                last_typing_time = current_time
                
        except pexpect.TIMEOUT:
            # When output pauses for 1.0s, process and send the buffer if it has content
            if buffer.strip():
                clean = clean_text(buffer)
                # Filter out the empty CLI prompts to reduce noise in Telegram
                if clean and not clean.endswith("For shortcuts"):
                    # We send as plain native text (no code block, no markdown escaping needed)
                    send_message(clean)
                buffer = ""
        except pexpect.EOF:
            print("Pexpect EOF")
            break
        except Exception as e:
            print(f"Pexpect error: {e}")
            break

def poll_telegram():
    global child
    offset = 0
    while True:
        url = f"{API_URL}/getUpdates?offset={offset}&timeout=30"
        try:
            response = urllib.request.urlopen(url, timeout=35)
            data = json.loads(response.read().decode())
            if not data.get("ok"):
                time.sleep(2)
                continue
            
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                
                message = update.get("message")
                if not message:
                    continue
                
                if str(message.get("chat", {}).get("id")) != CHAT_ID:
                    continue # Ignore unauthorized users
                
                # Handle text
                if "text" in message:
                    text = message["text"]
                    if child and child.isalive():
                        child.sendline(text)
                
                # Handle photos
                elif "photo" in message:
                    # Get the highest resolution photo
                    photo = message["photo"][-1]
                    file_id = photo["file_id"]
                    file_url = get_file_url(file_id)
                    if file_url:
                        os.makedirs(UPLOAD_DIR, exist_ok=True)
                        dest = os.path.join(UPLOAD_DIR, f"tg_{file_id}.jpg")
                        if download_file(file_url, dest):
                            if child and child.isalive():
                                child.sendline(f"/upload {dest}")
                            send_message("📸 *Image received and passed to Antigravity CLI.*")
                        
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    print("Starting Telegram bridge...")
    
    t1 = threading.Thread(target=pexpect_thread, daemon=True)
    t1.start()
    
    poll_telegram()
