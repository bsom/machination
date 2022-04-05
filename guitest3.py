import sys
from ctypes import windll

windll.user32.SetProcessDpiAwarenessContext(-4)

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

from colors import rgb
from colors import hex as _hex

import mido

from func_timeout import func_timeout, FunctionTimedOut

from typing import List, Any

from kivy.config import Config
Config.set('graphics','borderless',1)
Config.set('graphics', 'width', 1920)
Config.set('graphics', 'height', 1080)
Config.set('graphics', 'resizable', 0)
Config.write()

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import ColorProperty

all_clip_colors = {
        "0xee97a5": 1, "0xf0a648": 2, "0xc29841": 3, "0xf7f28a": 4, "0xccf84e": 5, "0x7dfa57": 6, "0x7efaad": 7,
        "0x8ffbe7": 8, "0x96c3fa": 9, "0x5d80dc":10, "0x94a6f9":11, "0xc773dd":12, "0xd15e9c":13, "0xffffff":14,
        "0xe84a42":15, "0xe27230":16, "0x917251":17, "0xfdee5c":18, "0xa7fb7a":19, "0x6abe3a":20, "0x5abbad":21,
        "0x70e5fc":22, "0x4ea1e7":23, "0x3a7bb9":24, "0x816fdc":25, "0xaa7ac0":26, "0xe750cd":27, "0xcfcfcf":28,
        "0xd06d5f":29, "0xf0a47b":30, "0xcbac78":31, "0xf0fdb5":32, "0xd5e29e":33, "0xbdcd7d":34, "0xa3c190":35,
        "0xdcfbe2":36, "0xd3f0f7":37, "0xb9c0df":38, "0xc8bbe0":39, "0xa899df":40, "0xe2dbe0":41, "0xa7a7a7":42,
        "0xbc928b":43, "0xad825c":44, "0x93826c":45, "0xbdb872":46, "0xaaba3c":47, "0x88ac5a":48, "0x94bfb8":49,
        "0x9eb1c1":50, "0x8aa3be":51, "0x8492c6":52, "0xa094b1":53, "0xb79fba":54, "0xaf7493":55, "0x7a7a7a":56,
        "0x9e3e3a":57, "0x9b553b":58, "0x6c5145":59, "0xd6c140":60, "0x879339":61, "0x689b43":62, "0x4b988c":63,
        "0x396280":64, "0x23358f":65, "0x39549b":66, "0x5d4fa6":67, "0x9553a6":68, "0xb83f6d":69, "0x3e3e3e":70
        }


Builder.load_string('''
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
        Button:
            id: button1
            text: root.button1Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button1Color
            color: 1,1,1,1
            markup: True
        Button:
            id: button2
            text: root.button2Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button2Color
            color: 1,1,1,1
            markup: True
        Button:
            id: button3
            text: root.button3Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button3Color
            color: 1,1,1,1
            markup: True
        Button:
            id: button4
            text: root.button4Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button4Color
            color: 1,1,1,1
            markup: True
        Button:
            id: button5
            text: root.button5Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button5Color
            color: 1,1,1,1
            markup: True
        Button:
            id: button6
            text: root.button6Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button6Color
            color: 1,1,1,1
            markup: True
        Button:
            id: button7
            text: root.button7Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button7Color
            color: 1,1,1,1
            markup: True
        Button:
            id: button8
            text: root.button8Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button8Color
            color: 1,1,1,1
            markup: True
    GridLayout:
        orientation: 'lr-tb'
        cols: 1
        rows: 1
        size_hint_y:0.05
        size_hint_x:1.0
        Label:
            id: statusLabel
            text: root.statusLabelText
            halign:'left'
            max_lines:1
            font_size:25
    GridLayout:
        orientation: 'lr-tb'
        cols: 3
        rows: 1
        size_hint_y:0.1
        Button:
            id: buttonID
            text:"bsom:know_future:version102"
            halign:'right'
            max_lines:4
            font_size:25
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
''')


class pyMachination(App):
    def build(self):

        osc.setup()
        osc.get_version()
        osc.get_tempo()

        print("Getting clip names...")
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
    button1Color = ColorProperty([0.1,0.1,0.1,1])
    button2Color = ColorProperty([0.1,0.1,0.1,1])
    button3Color = ColorProperty([0.1,0.1,0.1,1])
    button4Color = ColorProperty([0.1,0.1,0.1,1])
    button5Color = ColorProperty([0.1,0.1,0.1,1])
    button6Color = ColorProperty([0.1,0.1,0.1,1])
    button7Color = ColorProperty([0.1,0.1,0.1,1])
    button8Color = ColorProperty([0.1,0.1,0.1,1])
    statusLabelText = StringProperty('....')

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
        setattr(rootObj,buttonToChange+"Text", "[color=#" + text_color + "]" + str(value) + ": " + str(osc.clips[knob-1][value])+"[/color]")
        setattr(rootObj,"statusLabelText", "Encoder: " + str(knob) + " Value: " + str(value) + " " + str(osc.clips[knob-1][value]) + " Color: " + str(hexcolor))

        if hexcolor in all_clip_colors:
            clip_number = all_clip_colors.get(hexcolor)
            outMessage = mido.Message('control_change',channel=knob-1,control=1,value=clip_number)
            OutToTeensy.send(outMessage)
        else:
            outMessage = mido.Message('control_change',channel=knob-1,control=1,value=61)
            OutToTeensy.send(outMessage)
        

if __name__ == '__main__':
    osc = know_future()
    pyMachination().run()
