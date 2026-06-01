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
        # Filter out CLI prompts
        if line and line not in ['?', '>'] and "For shortcuts" not in line:
            final_lines.append(line)
            
    return '\n'.join(final_lines)

def clean_text(text):
    text = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)
    final_lines = []
    for line in text.split('\n'):
        parts = line.split('\r')
        line = parts[-1]
        while '\b' in line:
            new_line = re.sub(r'[^\b]\b', '', line)
            if new_line == line:
                line = line.lstrip('\b')
                break
            line = new_line
        line = line.strip()
        if line and line not in ['?', '>'] and "For shortcuts" not in line:
            final_lines.append(line)
    return '\n'.join(final_lines)

def send_message(text, parse_mode=None):
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    if parse_mode:
        data["parse_mode"] = parse_mode
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try: urllib.request.urlopen(req)
    except: pass

def send_typing_action():
    url = f"{API_URL}/sendChatAction"
    data = {"chat_id": CHAT_ID, "action": "typing"}
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try: urllib.request.urlopen(req)
    except: pass

def get_file_url(file_id):
    url = f"{API_URL}/getFile?file_id={file_id}"
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())
        if data.get("ok"):
            return f"https://api.telegram.org/file/bot{TOKEN}/{data['result']['file_path']}"
    except: pass
    return None

def download_file(url, dest_path):
    try:
        urllib.request.urlretrieve(url, dest_path)
        return True
    except: return False

def start_cli():
    print("Starting CLI session...")
    child = pexpect.spawn('/usr/local/bin/agy', env={"NO_COLOR": "1", "TERM": "xterm-256color", **os.environ}, encoding='utf-8', dimensions=(50, 100))
    # Wait for the splash screen and first prompt to finish before we start answering Telegram
    try:
        child.expect([r'\? For shortcuts', r'> '], timeout=30)
        print("CLI is ready and waiting for commands.")
    except Exception as e:
        print(f"Failed to wait for initial CLI prompt: {e}")
    return child

def poll_telegram():
    child = start_cli()
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
                if not message: continue
                if str(message.get("chat", {}).get("id")) != CHAT_ID: continue
                
                # Check if CLI is still alive, restart if dead
                if not child.isalive():
                    print("CLI is dead, restarting...")
                    child = start_cli()
                
                text = ""
                if "text" in message:
                    text = message["text"]
                elif "photo" in message:
                    photo = message["photo"][-1]
                    file_id = photo["file_id"]
                    file_url = get_file_url(file_id)
                    if file_url:
                        os.makedirs(UPLOAD_DIR, exist_ok=True)
                        dest = os.path.join(UPLOAD_DIR, f"tg_{file_id}.jpg")
                        if download_file(file_url, dest):
                            text = f"/upload {dest}"
                            send_message("📸 *Imagen recibida.*", parse_mode="Markdown")
                
                if text:
                    send_typing_action()
                    child.sendline(text)
                    
                    try:
                        # Wait for the next prompt indicating the CLI has finished responding
                        child.expect([r'\? For shortcuts', r'> '], timeout=120)
                        
                        raw_output = child.before
                        clean = clean_text(raw_output)
                        
                        # Remove the echoed command itself
                        if clean.startswith(text):
                            clean = clean[len(text):].strip()
                            
                        if clean:
                            send_message(clean)
                            
                    except pexpect.TIMEOUT:
                        send_message("⚠️ The CLI took too long to respond.")
                        # Reset child to avoid corrupted states
                        child.close(force=True)
                        child = start_cli()
                    except pexpect.EOF:
                        send_message("⚠️ The CLI crashed while responding.")
                        child = start_cli()
                        
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    print("Starting Telegram bridge in synchronous mode...")
    poll_telegram()
