# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from asyncio import create_task, gather, run
from asyncio import sleep as async_sleep

import board
import time
import microcontroller
import adafruit_qmc5883p
import neopixel
import mdns
import socketpool
import math
import os, wifi

# MOTOR DRIVER
import pwmio
from adafruit_motor import motor

PWM_PIN_A = board.RX
PWM_PIN_B = board.SCK
pwm_a = pwmio.PWMOut(PWM_PIN_A, frequency=50)
pwm_b = pwmio.PWMOut(PWM_PIN_B, frequency=50)
motor1 = motor.DCMotor(pwm_a, pwm_b)
print("\nForwards slow")
motor1.throttle = 0.5
print("  throttle:", motor1.throttle)
time.sleep(1)

print("\nStop")
motor1.throttle = 0
print("  throttle:", motor1.throttle)
time.sleep(1)


i2c = board.STEMMA_I2C()
sensor = adafruit_qmc5883p.QMC5883P(i2c)

from adafruit_httpserver import GET, FileResponse, Request, Response, Server, Websocket
#import os, wifi
print("connecting...")
#wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
#   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
#print("my IP addr:", wifi.radio.ipv4_address)

AP_SSID = "RadioShack"
AP_PASSWORD = "RadioShack"

print("Creating access point...")
wifi.radio.start_ap(ssid=AP_SSID, password=AP_PASSWORD)
print(f"Created access point {AP_SSID}")

mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = "radioshack"
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=80)    #port=5000
#wifi.radio.hostname = "radioshack"

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

# pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
print("ap ip", wifi.radio.ipv4_address_ap)

websocket: Websocket = None

HTML_TEMPLATE = """
<!DOCTYPE html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>Soft Cars</title>
    <style>
        body {
            font-family: Courier, monospace; 
            background:HotPink;
            text-align: center;
            color:Snow;
        }
        input[type="button"] {
            font-family: Courier, monospace;
            background-color:MistyRose; 
            color:Orchid;
            font-size: 48px;
            height: 80px;
            margin: 10px;
            border: 3px solid black;
            border-radius: 20px;
        }
    </style>
    </head>
    <body>
        
        <h1>Soft Cars Remote Control</h1>
    	<input id="fwd" type="button" value="Forward">
        <input id="l" type="button" value="Left">
    	<input id="r" type="button" value="Right">
    	<input id="bwd" type="button" value="Backward">
    	<input id="stop" type="button" value="Stop">
    	<input id="honk" type="button" value="Honk">
    	<input id="flash" type="button" value="Flash">
        
        <p>CPU temperature: <strong>-</strong>&deg;C</p>
        <p>NeoPixel Color: <input type="color"></p>

        <script>
            const cpuTemp = document.querySelector('strong');
            const colorPicker = document.querySelector('input[type="color"]');
            

			let fwd = document.querySelector('input[id="fwd"]');
			fwd.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'forward': 1 } ))
  				ws.send(JSON.stringify( { 'forward': 1 } ));
			}, false);
			
			let bwd = document.querySelector('input[id="bwd"]');
			bwd.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'backward': 1 } ))
  				ws.send(JSON.stringify( { 'backward': 1 } ));
			}, false);

			let l = document.querySelector('input[id="l"]');
			l.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'left': 1 } ))
  				ws.send(JSON.stringify( { 'left': 1 } ));
			}, false);

            let r = document.querySelector('input[id="r"]');
			r.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'right': 1 } ))
  				ws.send(JSON.stringify( { 'right': 1 } ));
			}, false);

            let stop = document.querySelector('input[id="stop"]');
			stop.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'stop': 1 } ))
  				ws.send(JSON.stringify( { 'stop': 1 } ));
			}, false);

            let honk = document.querySelector('input[id="honk"]');
			honk.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'honk': 1 } ))
  				ws.send(JSON.stringify( { 'honk': 1 } ));
			}, false);

            let flash = document.querySelector('input[id="flash"]');
			honk.addEventListener('input', (event) => {
				console.log(JSON.stringify( { 'flash': 1 } ))
  				ws.send(JSON.stringify( { 'flash': 1 } ));
			}, false);
            
            let ws = new WebSocket('ws://' + location.host + '/connect-websocket');

            ws.onopen = () => console.log('WebSocket connection opened');
            ws.onclose = () => console.log('WebSocket connection closed');
            ws.onmessage = event => cpuTemp.textContent = event.data;
            ws.onerror = error => cpuTemp.textContent = error;

            colorPicker.oninput = debounce(() => ws.send(colorPicker.value), 200);

            function debounce(callback, delay = 1000) {
                let timeout
                return (...args) => {
                    clearTimeout(timeout)
                    timeout = setTimeout(() => {
                    callback(...args)
                  }, delay)
                }
            }
        </script>
    </body>
</html>
"""

@server.route("/", GET)
def client(request: Request):
	# return FileResponse(request, "index.html")
    return Response(request, HTML_TEMPLATE, content_type="text/html")


@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket

    if websocket is not None:
        websocket.close()  # Close any existing connection

    websocket = Websocket(request)

    return websocket


server.start(str(wifi.radio.ipv4_address_ap), 80)
# server.serve_forever(str(wifi.radio.ipv4_address_ap), 80)
while True:


    time.sleep(0.125)
    mag_x, mag_y, mag_z = sensor.magnetic
    print("X: {:.2f} uT, Y: {:.2f} uT, Z: {:.2f} uT".format(mag_x, mag_y, mag_z))
    
    heading = math.atan2(mag_y, mag_x)
    if heading < 0:
        heading += 2 * math.pi
    print("Heading: {:.2f} degrees".format(math.degrees(heading) - 15))


async def handle_http_requests():
    while True:
        server.poll()
        await async_sleep(0)


async def handle_websocket_requests():
    while True:
        if websocket is not None:
            if (data := websocket.receive(fail_silently=True)) is not None:
                # r, g, b = int(data[1:3], 16), int(data[3:5], 16), int(data[5:7], 16)
                ddict = eval(data)	#option one convert str to dict with eval
                print(type(ddict), ddict)
#                 ddictkey = ddict.keys()
#                 print("dict key ", ddictkey)
                
#                 if "forward" in ddict:
#                 	print("moving forward ", ddict.get("forward"))
#                 if "backward" in ddict:
#                 	print("moving backward", ddict.get("backward"))
                if "left" in ddict:
                	print("moving left", ddict.get("left"))
                # pixel.fill((r, g, b))

        await async_sleep(0)


async def send_websocket_messages():
    while True:
        if websocket is not None:
            cpu_temp = round(microcontroller.cpu.temperature, 2)
            websocket.send_message(str(cpu_temp), fail_silently=True)

        await async_sleep(1)


async def main():
    await gather(
        create_task(handle_http_requests()),
        create_task(handle_websocket_requests()),
        create_task(send_websocket_messages()),
    )


run(main())
