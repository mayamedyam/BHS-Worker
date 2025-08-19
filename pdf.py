import requests
import os
import time
import json

DEVICE_ID = "mW61ImpRAeWi3Q3x6e3on6L9"
AUTH_KEY = "yoYiI16kt94J37Pxo0z8wElz"
ENDPOINT = "https://bhsotomat.nihatersoy.com/DevicePdfHandler.ashx"
PDF_DIR = "/home/pi/Desktop/BHS-Upgrader/pdf/"
BUTTON_COUNT = 8
INTERVAL = 30  # saniye

# İndirilen PDF’leri kaydetmek için dosya
TRACK_FILE = os.path.join(PDF_DIR, "downloaded.json")

# 1-8 klasörleri oluştur
for i in range(1, BUTTON_COUNT + 1):
    os.makedirs(os.path.join(PDF_DIR, str(i)), exist_ok=True)

# Daha önce indirilen PDF’leri yükle
if os.path.exists(TRACK_FILE):
    with open(TRACK_FILE, 'r') as f:
        downloaded = set(json.load(f))
else:
    downloaded = set()

def download_pdf(pdf_url, save_path):
    if os.path.exists(save_path):
        return
    r = requests.get(pdf_url, stream=True)
    if r.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"İndirildi: {save_path}")
    else:
        print(f"Hata: {pdf_url} ({r.status_code})")

while True:
    try:
        payload = {"id": DEVICE_ID, "authKey": AUTH_KEY}
        r = requests.post(ENDPOINT, json=payload)
        data = r.json()  # her button için PDF listesi

        for idx, pdf_list in enumerate(data):
            if not pdf_list:
                continue
            button_folder = os.path.join(PDF_DIR, str(idx + 1))
            for pdf_file in pdf_list:
                # Sadece daha önce indirilmemiş PDF’leri indir
                if pdf_file in downloaded:
                    continue

                pdf_url = f"https://bhsotomat.nihatersoy.com/uploads/{pdf_file}"
                save_path = os.path.join(button_folder, os.path.basename(pdf_file))
                download_pdf(pdf_url, save_path)

                downloaded.add(pdf_file)

        # Güncellenmiş indirilen PDF listesini kaydet
        with open(TRACK_FILE, 'w') as f:
            json.dump(list(downloaded), f)

    except Exception as e:
        print("Hata:", e)

    time.sleep(INTERVAL)
