import board
import time
import microcontroller
import os, wifi


print("INIT: Create RadioShack Access Point")
#wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
#   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
#print("my IP addr:", wifi.radio.ipv4_address)

AP_SSID = "RadioShack"
AP_PASSWORD = "RadioShack"

print("ATTEMPT: Create RadioShack Access Point")
wifi.radio.start_ap(ssid=AP_SSID, password=AP_PASSWORD)
print(f"SUCCESS: Created Access Point {AP_SSID}")

print("ACESS POINT IP: ", wifi.radio.ipv4_address_ap)
