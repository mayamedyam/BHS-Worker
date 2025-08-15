import requests as r
import datetime
import time
import os
import dotenv
import env_controller

class networkJobs:
    def __init__(self, device_id: str, auth_key: str):
        print(f"[NETWORK | MAIN] Network access creating using id:{device_id}")

        self._id = device_id
        self._authKey = auth_key
        self._setup_url = "https://bhsotomat.nihatersoy.com/apix/setupDevice.ashx"
        self._control_url = "https://bhsotomat.nihatersoy.com/apix/controlDevice.ashx"
        self._buttonCount_url = "https://bhsotomat.nihatersoy.com/apix/buttonCount.ashx"
        self._async_url = "https://bhsotomat.nihatersoy.com/apix/asyncFiles.ashx"
        self._downloadURL = "https://bhsotomat.nihatersoy.com/apix/downloadFile.ashx"
        self._versionLink = "https://bhsotomat.nihatersoy.com/apix/version.ashx"
        self._anyinfo_url = "https://bhsotomat.nihatersoy.com/apix/anydesk.ashx"
        self._clock_url = "https://bhsotomat.nihatersoy.com/apix/getclock.ashx"
        self._printer_status = "https://bhsotomat.nihatersoy.com/apix/change_printer_status.ashx"
        self._printer_information = "https://bhsotomat.nihatersoy.com/apix/get_printer_information.ashx"
        self._h = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        print(f"[NETWORK | MAIN] Network class generated")

        if self.is_connected():
            if not self.isRegistered():
                print("[DEBUG] Cihaz kayıtlı değil, setup başlatılıyor...")
                self.setup()
                print('Registiration Sent')
                while not self.isRegistered():
                    print('Waiting for system grant...')
                    time.sleep(5)

    def is_connected(self):
        try:
            r.get('https://www.google.com', timeout=5)
            return True
        except (r.ConnectionError, r.Timeout):
            return False

    def versionControl(self, version: str):
        try:
            if self.is_connected():
                response = r.get(self._versionLink)
                print("[DEBUG] Version control response:", response.status_code, response.text)
                if response.status_code == 200:
                    return response.text == version
                return True
            else:
                print('Version cannot be checked currently. No internet interface found')
                return True
        except Exception as e:
            print('-------------Version Control-------------')
            print(e)
            print('--------------------------')

    def setup(self) -> bool:
        try:
            if self.is_connected():
                time.sleep(3)
                setupCredentials = {
                    'id': self._id,
                    'authKey': self._authKey,
                    'wifiName': "Device Setup"
                }
                print("[DEBUG] Setup POST URL:", self._setup_url)
                print("[DEBUG] Setup POST JSON:", setupCredentials)

                response = r.post(self._setup_url, json=setupCredentials, headers=self._h)

                print("[DEBUG] Setup response status:", response.status_code)
                print("[DEBUG] Setup response body:", response.text)

                return response.status_code == 200
            else:
                print('Setup process failed due no internet connection')
                return False
        except Exception as e:
            print('-------------Setup Process-------------')
            print(e)
            print('--------------------------')
            return False

    def isRegistered(self) -> bool:
        setupCredentials = {
            'id': self._id,
            'authKey': self._authKey
        }
        try:
            if self.is_connected():
                print("[DEBUG] isRegistered kontrol ediliyor...")
                response = r.post(self._control_url, json=setupCredentials, headers=self._h)
                print("[DEBUG] isRegistered status:", response.status_code)
                print("[DEBUG] isRegistered raw response:", response.text)

                if response.text.strip() == '-D':
                    print("[DEBUG] Sunucu '-D' döndü, cihaz kayıtlı değil.")
                    return False

                try:
                    data = response.json()
                    validated = data.get('status') in [1, 2]
                    print("[DEBUG] isRegistered parsed JSON:", data)
                    return validated
                except ValueError:
                    print("[DEBUG] JSON parse hatası, gelen veri:", response.text)
                    return False
            else:
                print('Registration data is not available. Continuing for no network mode')
                return True
        except Exception as e:
            print('-------------Is Device Registered-------------')
            print(e)
            print('--------------------------')
            return True

    # Diğer fonksiyonlar aynı, sadece gerektiğinde benzer debug print ekleyebilirsin.
