APIKEY = "CFCAA7402B"

import colorsys
import json
import requests
import socketserver

class HueUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].decode()
        print("{} sent {}".format(self.client_address[0], data))
        light, rgb = data.split(",")
        set_light_state("1", rgb)
        

def set_light_state(light_id, rgb):
    rgb = int(rgb)
    if rgb == 0:
        print("Turning light {} off".format(light_id))
        request_data = {"on": False}
    else:
        red = rgb % 1000
        green = rgb // 1000 % 1000
        blue = rgb // 1000000

        hsv = colorsys.rgb_to_hsv(red / 100, green / 100, blue / 100)
        hue = int(hsv[0] * 65565)
        sat = int(hsv[1] * 255)
        bri = int(hsv[2] * 255)
        print("Setting light {} to HSV values {} {} {}"
              .format(light_id, hue, sat, bri))
        
        request_data = {"on": True, "hue": hue, "bri": bri, "sat": sat}
    
    r = requests.put("http://localhost/api/{}/lights/{}/state"
                     .format(APIKEY, light_id),
                     json=request_data)
    print("Response:", r.status_code)


def get_lights():
    r = requests.get("http://localhost/api/{}/lights".format(APIKEY))
    if r.status_code == 200:
        data = r.json()


if __name__ == "__main__":
    HOST, PORT = "", 7777
    print("establish UDP server ...")
    udp_server = socketserver.UDPServer((HOST, PORT), HueUDPHandler)
    udp_server.serve_forever()
