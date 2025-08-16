import requests as r
import os
import time
import json
from typing import List, Tuple

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
                while not self.isRegistered():
                    print('Waiting for system grant...')
                    time.sleep(5)

    def is_connected(self) -> bool:
        try:
            r.get('https://www.google.com', timeout=5)
            return True
        except (r.ConnectionError, r.Timeout):
            return False

    def setup(self) -> bool:
        try:
            if self.is_connected():
                time.sleep(3)
                setupCredentials = {'id': self._id, 'authKey': self._authKey, 'wifiName': "Device Setup"}
                response = r.post(self._setup_url, json=setupCredentials, headers=self._h)
                return response.status_code == 200
            else:
                return False
        except Exception as e:
            print("[ERROR] Setup failed:", e)
            return False

    def isRegistered(self) -> bool:
        try:
            payload = {'id': self._id, 'authKey': self._authKey}
            if self.is_connected():
                response = r.post(self._control_url, json=payload, headers=self._h)
                if response.text.strip() == '-D':
                    return False
                try:
                    data = response.json()
                    return data.get('status') in [1, 2]
                except ValueError:
                    return False
            else:
                return True
        except Exception as e:
            print("[ERROR] isRegistered:", e)
            return True

    def getWorkingTimes(self) -> List[List[str]]:
        """Cihazın çalışma saatlerini veritabanından çeker."""
        try:
            payload = {'id': self._id, 'authKey': self._authKey}
            response = r.post(self._control_url, json=payload, headers=self._h)
            data = response.json()
            # Örnek veri: {"deviceStartTime":"08:00","deviceEndTime":"12:00","device_second_StartTime":"13:00","device_second_EndTime":"17:00"}
            return [
                [data.get('deviceStartTime', '08:00'), data.get('deviceEndTime', '12:00')],
                [data.get('device_second_StartTime', '13:00'), data.get('device_second_EndTime', '17:00')]
            ]
        except Exception as e:
            print("[ERROR] getWorkingTimes:", e)
            # Default saatler
            return [['08:00', '12:00'], ['13:00', '17:00']]

    def getButtonCount(self) -> int:
        try:
            payload = {'id': self._id, 'authKey': self._authKey}
            response = r.post(self._buttonCount_url, json=payload, headers=self._h)
            data = response.json()
            return int(data.get('count', 8))
        except Exception as e:
            print("[ERROR] getButtonCount:", e)
            return 8

    def downloadFile(self, fileName: str) -> bytes:
        try:
            payload = {'id': self._id, 'authKey': self._authKey, 'fileName': fileName}
            response = r.post(self._downloadURL, json=payload, headers=self._h)
            if response.status_code == 200:
                return response.content
            else:
                return b''
        except Exception as e:
            print("[ERROR] downloadFile:", e)
            return b''

    def getAnyDeskInfo(self) -> dict:
        try:
            payload = {'id': self._id, 'authKey': self._authKey}
            response = r.post(self._anyinfo_url, json=payload, headers=self._h)
            return response.json()
        except Exception as e:
            print("[ERROR] getAnyDeskInfo:", e)
            return {}

    def getPrinterInfo(self) -> dict:
        try:
            payload = {'id': self._id, 'authKey': self._authKey}
            response = r.post(self._printer_information, json=payload, headers=self._h)
            return response.json()
        except Exception as e:
            print("[ERROR] getPrinterInfo:", e)
            return {}
