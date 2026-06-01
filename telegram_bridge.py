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

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def send_message(text, parse_mode="Markdown"):
    url = f"{API_URL}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": parse_mode
    }
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
    child = pexpect.spawn('dtach -A /tmp/agy_1.socket', encoding='utf-8', dimensions=(24, 80))
    
    buffer = ""
    last_typing_time = 0
    
    while True:
        try:
            char = child.read(1)
            if not char:
                break
            
            buffer += char
            
            # Send typing action every 3 seconds if buffer is accumulating
            current_time = time.time()
            if len(buffer) > 0 and current_time - last_typing_time > 3:
                send_typing_action()
                last_typing_time = current_time
            
            # Look for prompt indicators to flush the buffer
            # Antigravity CLI typically uses '>' or '?' or 'Select an option'
            if char in ['>', '?', '\n']:
                # Basic heuristic to flush output
                # We don't want to send single characters, we want blocks
                # We will wait for a tiny timeout to see if more data comes
                time.sleep(0.1)
                
                # Check if we have pending data to read using select or just a small timeout
                import select
                r, w, x = select.select([child], [], [], 0.1)
                if not r:
                    # No more data immediately available, flush buffer
                    text = strip_ansi(buffer).strip()
                    if text:
                        # Avoid sending just prompt characters
                        if text not in ['>', '?', '']:
                            # Very basic markdown escaping
                            text = text.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[')
                            send_message(f"```\n{text}\n```")
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
