import sys

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

from typing import List, Any

def printOutput(address: str, *args: List[Any]) -> None:
    print(*args)

def print_version(address: str, *args: List[Any]) -> None:
    print("Detected Ableton Live Version " + str(args[0]) + "." + str(args[1]))

def print_color(address:str, *args: List[Any]) -> None:
    print(hex(args[0]))
    #print()

dispatcher = Dispatcher()
dispatcher.map("/live/application/get/version", print_version)
dispatcher.map("/live/clip/get/color", print_color)
dispatcher.set_default_handler(printOutput)

print("Starting OSC server...")

server = BlockingOSCUDPServer(("127.0.0.1", 11001),dispatcher)
client = SimpleUDPClient("127.0.0.1", 11000)

client.send_message("/live/application/get/version",0)
server.handle_request()

track=0
clip=0
while clip < 70:
	client.send_message("/live/clip/get/color",(track, clip))
	#print("Track: " + str(track) + " Clip: " + str(clip))
	server.handle_request()
	clip=clip+1
