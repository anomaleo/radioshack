import socketpool
import wifi
import mdns

from adafruit_httpserver import Request, Response, Server

AP_SSID = "RadioShack"
AP_PASSWORD = "RadioShack"

print("Creating access point...")
wifi.radio.start_ap(ssid=AP_SSID, password=AP_PASSWORD)
print(f"Created access point {AP_SSID}")

mdns.Server(wifi.radio).hostname = "radioshack"
wifi.radio.hostname = "radioshack"

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)


@server.route("/")
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    return Response(request, "Hello from the CircuitPython HTTP Server!")


server.serve_forever(str(wifi.radio.ipv4_address_ap))