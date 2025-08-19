import os
import json
import time
import requests

from fileJobs import fileJobs  # Yukarıdaki class burada kullanılacak

DEVICE_ID = "mW61ImpRAeWi3Q3x6e3on6L9"
AUTH_KEY = "yoYiI16kt94J37Pxo0z8wElz"
ENDPOINT = "https://bhsotomat.nihatersoy.com/DevicePdfHandler.ashx"
INTERVAL = 30  # saniye

# PDF klasör kontrolü ve oluşturma
fj = fileJobs()
fj.generateFolders()

# Daha önce indirilen PDF’leri takip etmek için dosya
TRACK_FILE = os.path.join(fj.fileLocation, "downloaded.json")
if os.path.exists(TRACK_FILE):
    with open(TRACK_FILE, 'r') as f:
        downloaded = set(json.load(f))
else:
    downloaded = set()

def download_pdf(button: int, pdf_file: str):
    pdf_url = f"https://bhsotomat.nihatersoy.com/uploads/{pdf_file}"
    save_path = os.path.join(fj.fileLocation, str(button), os.path.basename(pdf_file))
    
    if os.path.exists(save_path):
        return
    
    r = requests.get(pdf_url, stream=True)
    if r.status_code == 200:
        fj.saveFile(button, os.path.splitext(os.path.basename(pdf_file))[0], r.content)
        print(f"[DOWNLOAD] {pdf_file} => Button {button}")
        downloaded.add(pdf_file)
    else:
        print(f"[ERROR] {pdf_file} indirilemedi ({r.status_code})")

# Sürekli kontrol döngüsü
while True:
    try:
        payload = {"id": DEVICE_ID, "authKey": AUTH_KEY}
        r = requests.post(ENDPOINT, json=payload)
        data = r.json()  # her button için PDF listesi
        
        for idx, pdf_list in enumerate(data):
            button = idx + 1
            if not pdf_list:
                continue
            for pdf_file in pdf_list:
                if pdf_file not in downloaded:
                    download_pdf(button, pdf_file)
        
        # Güncellenmiş indirilen PDF listesini kaydet
        with open(TRACK_FILE, 'w') as f:
            json.dump(list(downloaded), f)
            
    except Exception as e:
        print(f"[ERROR] {e}")
    
    time.sleep(INTERVAL)

bunu githuba mı atacaz