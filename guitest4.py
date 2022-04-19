import sys

# Make Kivy window Windows Scaling Aware
from ctypes import windll
windll.user32.SetProcessDpiAwarenessContext(-4)

# PythonOSC Dependencies
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

# Color Value Manipulation
from colors import rgb
from colors import hex as _hex

# MIDI I/O
import mido

# Function Timeout
from func_timeout import func_timeout, FunctionTimedOut

# List Manipulation
from typing import List, Any

# Kivy Window Config
from kivy.config import Config
Config.set('graphics','borderless',1)
Config.set('graphics', 'width', 1920)
Config.set('graphics', 'height', 1080)
Config.set('graphics', 'resizable', 0)
Config.write()

# Kivy Dependencies
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import ColorProperty

# Ableton Live 11 Clip Colors
all_clip_colors = {
		"0xff94a6": 1,"0xffa529": 2,"0xcc9927": 3,"0xf7f47c": 4,"0xbffb00": 5,"0x1aff2f": 6,"0x25ffa8": 7,
		"0x5cffe8": 8,"0x8bc5ff": 9,"0x5480e4":10,"0x92a7ff":11,"0xd86ce4":12,"0xe553a0":13,"0xffffff":14,
		"0xff3636":15,"0xf66c03":16,"0x99724b":17,"0xfff034":18,"0x87ff67":19,"0x3dc300":20,"0xbfaf":  21,
		"0x19e9ff":22,"0x10a4ee":23,"0x7dc0":  24,"0x886ce4":25,"0xb677c6":26,"0xff39d4":27,"0xd0d0d0":28,
		"0xe2675a":29,"0xffa374":30,"0xd3ad71":31,"0xedffae":32,"0xd2e498":33,"0xbad074":34,"0x9bc48d":35,
		"0xd4fde1":36,"0xcdf1f8":37,"0xb9c1e3":38,"0xcdbbe4":39,"0xae98e5":40,"0xe5dce1":41,"0xa9a9a9":42,
		"0xc6928b":43,"0xb78256":44,"0x99836a":45,"0xbfba69":46,"0xa6be00":47,"0x7db04d":48,"0x88c2ba":49,
		"0x9bb3c4":50,"0x85a5c2":51,"0x8393cc":52,"0xa595b5":53,"0xbf9fbe":54,"0xbc7196":55,"0x7b7b7b":56,
		"0xaf3333":57,"0xa95131":58,"0x724f41":59,"0xdbc300":60,"0x85961f":61,"0x539f31":62,"0xa9c8e": 63,
		"0x236384":64,"0x1a2f96":65,"0x2f52a2":66,"0x624bad":67,"0xa34bad":68,"0xcc2e6e":69,"0x3c3c3c":70}

# Kivy Window Builder
Builder.load_string("""
<mainWindow>:
    orientation: 'lr-tb'
    cols: 1
    rows: 3
    size_hint_y:1.0
    GridLayout:
        orientation: 'lr-tb'
        cols: 4
        rows: 2
        size_hint_y:1.0
        spacing: [20,20]
        Button:
            id: button1
            background_color: root.button1Color
            canvas:
                Color: 
                    rgb: root.button1Color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0,0,0,150]
                    segments: 1
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'left'
                anchor_y: 'bottom'
                Label:
                    text_size: self.width, None
                    text: root.button1Text
                    size_hint_y: None
                    size_hint_x: None
                    font_name: root.fontName
                    font_size: 32
                    padding: dp(12),dp(5)
                    markup: True
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'center'
                anchor_y: 'center'
                Label:
                    text_size: self.width, None
                    font_name: root.fontName
                    text: root.button1Text2
                    font_size: 64
                    padding: dp(70),dp(100)
                    size_hint_y: None
                    markup: True
                    halign: 'center'
        Button:
            id: button2
            background_color: root.button2Color
            canvas:
                Color: 
                    rgb: root.button2Color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0,0,0,150]
                    segments: 1
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'left'
                anchor_y: 'bottom'
                Label:
                    text_size: self.width, None
                    text: root.button2Text
                    size_hint_y: None
                    size_hint_x: None
                    font_name: root.fontName
                    font_size: 32
                    padding: dp(12),dp(5)
                    markup: True
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'center'
                anchor_y: 'center'
                Label:
                    text_size: self.width, None
                    font_name: root.fontName
                    text: root.button2Text2
                    font_size: 64
                    padding: dp(70),dp(100)
                    size_hint_y: None
                    markup: True
                    halign: 'center'
        Button:
            id: button3
            background_color: root.button3Color
            canvas:
                Color: 
                    rgb: root.button3Color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0,0,0,150]
                    segments: 1
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'left'
                anchor_y: 'bottom'
                Label:
                    text_size: self.width, None
                    text: root.button3Text
                    size_hint_y: None
                    size_hint_x: None
                    font_name: root.fontName
                    font_size: 32
                    padding: dp(12),dp(5)
                    markup: True
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'center'
                anchor_y: 'center'
                Label:
                    text_size: self.width, None
                    font_name: root.fontName
                    text: root.button3Text2
                    font_size: 64
                    padding: dp(70),dp(100)
                    size_hint_y: None
                    markup: True
                    halign: 'center'
        Button:
            id: button4
            background_color: root.button4Color
            canvas:
                Color: 
                    rgb: root.button4Color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0,0,0,150]
                    segments: 1
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'left'
                anchor_y: 'bottom'
                Label:
                    text_size: self.width, None
                    text: root.button4Text
                    size_hint_y: None
                    size_hint_x: None
                    font_name: root.fontName
                    font_size: 32
                    padding: dp(12),dp(5)
                    markup: True
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'center'
                anchor_y: 'center'
                Label:
                    text_size: self.width, None
                    font_name: root.fontName
                    text: root.button4Text2
                    font_size: 64
                    padding: dp(70),dp(100)
                    size_hint_y: None
                    markup: True
                    halign: 'center'
        Button:
            id: button5
            background_color: root.button5Color
            canvas:
                Color: 
                    rgb: root.button5Color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0,0,0,150]
                    segments: 1
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'left'
                anchor_y: 'bottom'
                Label:
                    text_size: self.width, None
                    text: root.button5Text
                    size_hint_y: None
                    size_hint_x: None
                    font_name: root.fontName
                    font_size: 32
                    padding: dp(12),dp(5)
                    markup: True
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'center'
                anchor_y: 'center'Label:
                    text_size: self.width, None
                    font_name: root.fontName
                    text: root.button5Text2
                    font_size: 64
                    padding: dp(70),dp(100)
                    size_hint_y: None
                    markup: True
                    halign: 'center'
        Button:
            id: button6
            background_color: root.button6Color
            canvas:
                Color: 
                    rgb: root.button6Color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0,0,0,150]
                    segments: 1
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'left'
                anchor_y: 'bottom'
                Label:
                    text_size: self.width, None
                    text: root.button6Text
                    size_hint_y: None
                    size_hint_x: None
                    font_name: root.fontName
                    font_size: 32
                    padding: dp(12),dp(5)
                    markup: True
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'center'
                anchor_y: 'center'
                Label:
                    text_size: self.width, None
                    font_name: root.fontName
                    text: root.button6Text2
                    font_size: 64
                    padding: dp(70),dp(100)
                    size_hint_y: None
                    markup: True
                    halign: 'center'
        Button:
            id: button7
            background_color: root.button7Color
            canvas:
                Color: 
                    rgb: root.button7Color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0,0,0,150]
                    segments: 1
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'left'
                anchor_y: 'bottom'
                Label:
                    text_size: self.width, None
                    text: root.button7Text
                    size_hint_y: None
                    size_hint_x: None
                    font_name: root.fontName
                    font_size: 32
                    padding: dp(12),dp(5)
                    markup: True
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'center'
                anchor_y: 'center'
                Label:
                    text_size: self.width, None
                    font_name: root.fontName
                    text: root.button7Text2
                    font_size: 64
                    padding: dp(70),dp(100)
                    size_hint_y: None
                    markup: True
                    halign: 'center'
        Button:
            id: button8
            background_color: root.button8Color
            canvas:
                Color: 
                    rgb: root.button8Color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0,0,0,150]
                    segments: 1
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'left'
                anchor_y: 'bottom'
                Label:
                    text_size: self.width, None
                    text: root.button8Text
                    size_hint_y: None
                    size_hint_x: None
                    font_name: root.fontName
                    font_size: 32
                    padding: dp(12),dp(5)
                    markup: True
            AnchorLayout:
                pos: self.parent.pos
                size: self.parent.size
                anchor_x: 'center'
                anchor_y: 'center'
                Label:
                    text_size: self.width, None
                    font_name: root.fontName
                    text: root.button8Text2
                    font_size: 64
                    padding: dp(70),dp(100)
                    size_hint_y: None
                    markup: True
                    halign: 'center'
    GridLayout:
        orientation: 'lr-tb'
        cols: 1
        rows: 1
        size_hint_y: 0.05
        size_hint_x: 1.0
        Label:
            id: statusLabel
            text: root.statusLabelText
            halign: 'left'
            max_lines: 1
            font_size: 25
    GridLayout:
        orientation: 'lr-tb'
        cols: 3
        rows: 1
        size_hint_y: 0.1
        Button:
            id: buttonID
            text: "bsom:know_future:version218"
            halign: 'right'
            max_lines: 4
            font_size: 25
            background_color: 0.4,0.4,0.4,1
        Button:
            id: buttonPlay
            text: "Play"
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: 0,1,0,1
            color: 0,0,0,1
            markup: True
        Button:
            id: buttonStop
            text: "Stop"
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: 1,0,0,1
            color: 0,0,0,1
            markup: True
            """)

class pyMachination(App):
	def build(self):

		# Setup/Start OSC
		osc.setup()
		osc.get_version()
		osc.get_tempo()

		#Get Clip Names and colors
		print("Getting clip names and colors...")
		for track in range(8):
			print("Scanning Track " + str(track+1))
			for clip in range (127):
				try:
					func_timeout(1,osc.getclipname,args=(track,clip))
				except FunctionTimedOut:
					break
					continue
				try:
					func_timeout(1,osc.getclipcolor,args=(track,clip))
				except FunctionTimedOut:
					break
					continue

		self.main_screen = mainWindow()

		return self.main_screen


class know_future:

	def setup(self):
		self.clips = []
		self.clip_colors = []
		self.current_track = 0
		self.current_clip = 0
		for j in range(8):
			column_clips=[]
			column_color=[]
			for k in range(128):
				column_clips.append("empty")
				column_color.append(0x191919)
			self.clips.append(column_clips)
			self.clip_colors.append(column_color)
		self.dispatcher = Dispatcher()
		self.dispatcher.map("/live/application/get/version", self.printOutput, "version")
		self.dispatcher.map("/live/song/get/tempo", self.printOutput, "tempo")
		self.dispatcher.map("/live/clip/get/name", self.printOutput, "clip_name")
		self.dispatcher.map("/live/clip/get/color", self.printOutput, "clip_color")
		self.dispatcher.map("/live/clip/fire", self.printOutput, "clip_fire")
		self.dispatcher.set_default_handler(self.printOutput)
		self.start_server()


	def printOutput(self, address: str, *args: List[Any]) -> None:
		if args[0] == ['version']:
			print("Detected Ableton Live Version " + str(args[1]) + "." + str(args[2]))
		elif args[0] == ['tempo']:
			print("Current tempo: " + str(args[1]))
		elif args[0] == ['clip_name']:
			print("Track: " + str(self.current_track+1) + " Clip " + str(self.current_clip+1) + " name: " + str(args[1]))
			self.clips[self.current_track][self.current_clip]=str(args[1])
		elif args[0] == ['clip_color']:
			print("Clip color: " + str(hex(args[1])))
			self.clip_colors[self.current_track][self.current_clip]=args[1]
		elif args[0] == ['clip_fire']:
			print(*args)
		else:
			print(*args)


	def getclipname(self,track,clip):
		self.current_clip = clip
		self.current_track = track
		self.client.send_message("/live/clip/get/name",(track,clip))
		self.server.handle_request()

	def getclipcolor(self,track,clip):
		self.current_clip = clip
		self.current_track = track
		self.client.send_message("/live/clip/get/color",(track,clip))
		self.server.handle_request()

	def start_server(self):
		print("Starting OSC server...")
		self.server = BlockingOSCUDPServer(("127.0.0.1", 11001),self.dispatcher)
		self.client = SimpleUDPClient("127.0.0.1", 11000)

	def get_version(self):
		self.client.send_message("/live/application/get/version",0)
		self.server.handle_request()

	def get_tempo(self):
		self.client.send_message("/live/song/get/tempo",0)
		self.server.handle_request()

	def get_clip_and_color(self, track, clip):
		self.getclipname(self,track,clip)
		self.getclipcolor(self,track,clip)

def hex_to_rgb(hexcolor):
	hexcolor = hexcolor.zfill(6)
	rgbcolor = tuple(_hex(hexcolor).rgb)
	rgbcolor = tuple(ti/255.0 for ti in rgbcolor)
	return rgbcolor

def relay_message(message):
	knob = message.channel
	value = message.note
	print("Knob, type, value: " + str(knob) + " " + str(message.type) + " " + str(value))
	if knob < 8:
		print("Fire!")
		osc.client.send_message("/live/clip/fire",(knob,value))
	else:
		mainWindow.update_button(mainWindow,knob-7,value)

OutToTeensy = mido.open_output('Machination 1')
InFromTeensy = mido.open_input('Machination 0', callback=relay_message)


switch = {
	1: "button1",
	2: "button2",
	3: "button3",
	4: "button4",
	5: "button5",
	6: "button6",
	7: "button7",
	8: "button8"
}


class mainWindow(GridLayout):
	button1Text = StringProperty('1')
	button2Text = StringProperty('2')
	button3Text = StringProperty('3')
	button4Text = StringProperty('4')
	button5Text = StringProperty('5')
	button6Text = StringProperty('6')
	button7Text = StringProperty('7')
	button8Text = StringProperty('8')
	button1Text2 = StringProperty('empty')
	button2Text2 = StringProperty('empty')
	button3Text2 = StringProperty('empty')
	button4Text2 = StringProperty('empty')
	button5Text2 = StringProperty('empty')
	button6Text2 = StringProperty('empty')
	button7Text2 = StringProperty('empty')
	button8Text2 = StringProperty('empty')
	button1Color = ColorProperty([0.1,0.1,0.1,1])
	button2Color = ColorProperty([0.1,0.1,0.1,1])
	button3Color = ColorProperty([0.1,0.1,0.1,1])
	button4Color = ColorProperty([0.1,0.1,0.1,1])
	button5Color = ColorProperty([0.1,0.1,0.1,1])
	button6Color = ColorProperty([0.1,0.1,0.1,1])
	button7Color = ColorProperty([0.1,0.1,0.1,1])
	button8Color = ColorProperty([0.1,0.1,0.1,1])
	statusLabelText = StringProperty('....')
	fontName = StringProperty('data-latin.ttf')

	def __init__(self, **kwargs):
		super(mainWindow, self).__init__(**kwargs)

	def update_button(self,knob,value):
		rootObj = App.get_running_app().root
		buttonToChange = switch.get(knob)
		hexcolor = str(hex(osc.clip_colors[knob-1][value]))
		if hexcolor != "0x191919":
			rgbcolor = hex_to_rgb(hexcolor.lstrip('0x'))
			rgbcolor = rgbcolor+(1,)
			text_color = "000000"
		else:
			rgbcolor = (0.1,0.1,0.1,1)
			text_color="ffffff"
		setattr(rootObj,buttonToChange+"Color",rgbcolor)
		setattr(rootObj,buttonToChange+"Text", "[color=#" + text_color + "]" + str(value) + "[/color]")
		setattr(rootObj,buttonToChange+"Text2", "[color=#" + text_color + "]" + str(osc.clips[knob-1][value])+"[/color]")
		setattr(rootObj,"statusLabelText", "Encoder: " + str(knob) + " Value: " + str(value) + " " + str(osc.clips[knob-1][value]))

		if hexcolor in all_clip_colors:
			clip_number = all_clip_colors.get(hexcolor)
			outMessage = mido.Message('control_change',channel=knob-1,control=1,value=clip_number)
			OutToTeensy.send(outMessage)
		else:
			outMessage = mido.Message('control_change',channel=knob-1,control=1,value=71)
			OutToTeensy.send(outMessage)


if __name__ == '__main__':
	osc = know_future()
	pyMachination().run()
