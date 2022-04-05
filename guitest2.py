import sys

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

from colors import rgb
from colors import hex as _hex

import mido

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

clip_colors = {
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
    cols: 4
    rows: 2
    GridLayout:
        orientation: 'lr-tb'
        cols: 4
        rows: 2
        Button:
            id: button1
            text: root.button1Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button1Color
            color: 0,0,0,1
            markup: True
        Button:
            id: button2
            text: root.button2Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button2Color
            color: 0,0,0,1
            markup: True
        Button:
            id: button3
            text: root.button3Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button3Color
            color: 0,0,0,1
            markup: True
        Button:
            id: button4
            text: root.button4Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button4Color
            color: 0,0,0,1
            markup: True
        Button:
            id: button5
            text: root.button5Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button5Color
            color: 0,0,0,1
            markup: True
        Button:
            id: button6
            text: root.button6Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button6Color
            color: 0,0,0,1
            markup: True
        Button:
            id: button7
            text: root.button7Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button7Color
            color: 0,0,0,1
            markup: True
        Button:
            id: button8
            text: root.button8Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button8Color
            color: 0,0,0,1
            markup: True
''')

from func_timeout import func_timeout, FunctionTimedOut

clips = []
for j in range(8):
    column=[]
    for k in range(128):
        column.append(("empty",0x191919))
    clips.append(column)

def printOutput(address: str, *args: List[Any]) -> None:
    clips[args[0]][args[1]]=(args[2],args[3])
    print("Track:" + str(args[0] + 1) + " | Clip:" + str(args[1] + 1) + " | Clip name:" + args[2] + " | Color:" + str(hex(args[3])))


def getclipname(server,client,track,clip):
    client.send_message("/live/name/clip",(track,clip))
    server.handle_request()

def hex_to_rgb(hexcolor):
    hexcolor = hexcolor.zfill(6)
    rgbcolor = tuple(_hex(hexcolor).rgb)
    rgbcolor = tuple(ti/255.0 for ti in rgbcolor)
    return rgbcolor

def relay_message(message):
    if message.type == 'note_on' and message.channel > 8 and message.velocity == 127:
        OutToAbleton.send(message)
    knob = message.channel
    value = message.note
    if knob > 7:
        mainWindow.update_button(mainWindow,knob-7,value)
    

OutToAbleton = mido.open_output('OutToAbleton 2')
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
    button1Text = StringProperty('Encoder 1')
    button2Text = StringProperty('Encoder 2')
    button3Text = StringProperty('Encoder 3')
    button4Text = StringProperty('Encoder 4')
    button5Text = StringProperty('Encoder 5')
    button6Text = StringProperty('Encoder 6')
    button7Text = StringProperty('Encoder 7')
    button8Text = StringProperty('Encoder 8')
    button1Color = ColorProperty([0.1,0.1,0.1,1])
    button2Color = ColorProperty([0.1,0.1,0.1,1])
    button3Color = ColorProperty([0.1,0.1,0.1,1])
    button4Color = ColorProperty([0.1,0.1,0.1,1])
    button5Color = ColorProperty([0.1,0.1,0.1,1])
    button6Color = ColorProperty([0.1,0.1,0.1,1])
    button7Color = ColorProperty([0.1,0.1,0.1,1])
    button8Color = ColorProperty([0.1,0.1,0.1,1])

    def __init__(self, **kwargs):
        super(mainWindow, self).__init__(**kwargs)
        
    def update_button(self,knob,value):
        buttonToChange = switch.get(knob)
        rootObj = App.get_running_app().root
        hexcolor = str(hex(clips[knob-1][value][1]))
        if hexcolor != "0x191919":
            rgbcolor = hex_to_rgb(hexcolor.lstrip('0x'))
            rgbcolor = rgbcolor+(1,)
            text_color = "000000"
        else:
            rgbcolor = (0.1,0.1,0.1,1)
            text_color="ffffff"
        setattr(rootObj,buttonToChange+"Color",rgbcolor)
        setattr(rootObj,buttonToChange+"Text", "[color=#" + text_color + "]Encoder " + str(knob) + "\nValue: " + str(value)+"\n"+str(clips[knob-1][value][0])+"[/color]")

        if hexcolor in clip_colors:
            clip_number = clip_colors.get(hexcolor)
            outMessage = mido.Message('control_change',channel=knob-1,control=1,value=clip_number)
            OutToTeensy.send(outMessage)
        else:
            outMessage = mido.Message('control_change',channel=knob-1,control=1,value=61)
            OutToTeensy.send(outMessage)
        
        
class pyMachination(App):
    def build(self):

        self.main_screen = mainWindow()

        dispatcher = Dispatcher()
        dispatcher.set_default_handler(printOutput)

        server = BlockingOSCUDPServer(("127.0.0.1", 9001),dispatcher)
        client = SimpleUDPClient("127.0.0.1", 9000)

        print("Getting clip names...")
        for track in range(8):
            print("Scanning Track " + str(track+1))
            for clip in range (127):
                try:
                    func_timeout(0.25,getclipname,args=(server,client,track,clip))
                except FunctionTimedOut:
                    break
                    continue
                

        return self.main_screen
        
        

if __name__ == '__main__':
    pyMachination().run()
