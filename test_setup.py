import requests

# API adresin
url = "https://bhsotomat.nihatersoy.com/apix/setupDevice.ashx"

# Test için göndereceğimiz JSON body
payload = {
    "id": "TEST_DEVICE_001",
    "authKey": "ABC123456",
    "wifiName": "MyTestWiFi"
}

# Header
headers = {
    "Content-Type": "application/json",
    "Accept": "text/plain"
}

try:
    print("[DEBUG] POST URL:", url)
    print("[DEBUG] POST DATA:", payload)

    response = requests.post(url, json=payload, headers=headers)

    print("[DEBUG] Status Code:", response.status_code)
    print("[DEBUG] Response Body:", response.text)

except Exception as e:
    print("[ERROR] Request failed:", e)
