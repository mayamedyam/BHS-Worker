import requests
import os
import time

# Cihaz ID ve AuthKey
DEVICE_ID = "mW61ImpRAeWi3Q3x6e3on6L9"
AUTH_KEY = "yoYiI16kt94J37Pxo0z8wElz"

# ASHX endpoint URL
ENDPOINT = "https://bhsotomat.nihatersoy.com/apix/DevicePdfHandler.ashx"

# Raspberry Pi üzerinde PDF ana klasörü
PDF_DIR = "/home/pi/Desktop/BHS-Upgrader/pdf/"

# Button sayısı
BUTTON_COUNT = 8

# 1-8 arası klasörleri oluştur
for i in range(1, BUTTON_COUNT + 1):
    folder_path = os.path.join(PDF_DIR, str(i))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# PDF kontrol aralığı (saniye)
INTERVAL = 30

# PDF indirme fonksiyonu
def download_pdf(pdf_url, save_path):
    if os.path.exists(save_path):
        return  # Zaten varsa indirme
    r = requests.get(pdf_url, stream=True)
    if r.status_code == 200:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"İndirildi: {save_path}")
    else:
        print(f"Hata: {pdf_url} {r.status_code}")

while True:
    try:
        # ASHX endpoint’ten JSON al
        payload = {"id": DEVICE_ID, "authKey": AUTH_KEY}
        r = requests.post(ENDPOINT, json=payload)
        data = r.json()  # JSON: list of lists, her button için PDF listesi

        for idx, pdf_list in enumerate(data):
            if not pdf_list:
                continue  # aktif değilse atla
            button_folder = os.path.join(PDF_DIR, str(idx + 1))
            for pdf_file in pdf_list:
                pdf_url = f"https://bhsotomat.nihatersoy.com/uploads/{pdf_file}"  # URL yolu
                save_path = os.path.join(button_folder, os.path.basename(pdf_file))
                download_pdf(pdf_url, save_path)

    except Exception as e:
        print("Hata:", e)

    time.sleep(INTERVAL)
