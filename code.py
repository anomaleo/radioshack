# https://github.com/adafruit/Adafruit_CircuitPython_HTTPServer/blob/main/examples/httpserver_start_and_poll.py
# https://github.com/adafruit/Adafruit_CircuitPython_HTTPServer/blob/main/examples/httpserver_start_and_poll_asyncio.py
import board
import time
import microcontroller
import neopixel
import mdns
import socketpool
import math
import os, wifi

# RADIOSHACK ACCESS POINT
import radioshack_create_access_point
print("ACESS POINT IP: ", wifi.radio.ipv4_address_ap)

# RADIOSHACK HTTP SERVER & WEBSOCKET
from adafruit_httpserver import GET, FileResponse, Request, Response, Server, Websocket, REQUEST_HANDLED_RESPONSE_SENT
from asyncio import create_task, gather, run
from asyncio import sleep as async_sleep

mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = "radioshack"
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=80)    #port=5000
#wifi.radio.hostname = "radioshack"

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

websocket: Websocket = None

# RADIOSHACK HTML WEBPAGE
from radioshack_www_html import HTML_TEMPLATE

# MOTOR DRIVER
from radioshack_motors import motors, left, right, stop, forward, backward

# MAGNETOMETER
import adafruit_qmc5883p
i2c = board.STEMMA_I2C()
sensor = adafruit_qmc5883p.QMC5883P(i2c)


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

# OPTION ONE: START AND POLL HTTP SERVER - NON ASYNC 
# while True:
#     try:
#         # Do something useful in this section,
#         # for example read a sensor and capture an average,
#         # or a running total of the last 10 samples
#         # print("waiting for a client")
#         # Process any waiting requests
#         pool_result = server.poll()
# 
#         if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
#             # Do something only after handling a request
#             print("not waiting for a client")
#             pass
# 
#         # If you want you can stop the server by calling server.stop() anywhere in your code
#     except OSError as error:
#         print(error)
#         continue

# OPTION TWO: START AND POLL HTTP SERVER - ASYNC 
async def handle_http_requests():
    while True:
        # Process any waiting requests
        # print("waiting for a client")
        pool_result = server.poll()

        if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
            # Do something only after handling a request
            pass

        await async_sleep(0)


async def act_on_websokect_msg():
    while True:
        # Do something useful in this section,
        # for example read a sensor and capture an average,
        # or a running total of the last 10 samples
        print("want to do something cool")
        
        await async_sleep(1)
        # If you want you can stop the server by calling server.stop() anywhere in your code


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
        create_task(act_on_websokect_msg()),
        create_task(send_websocket_messages()),
    )


run(main())
