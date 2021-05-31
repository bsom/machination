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
        "0xed4325": 1,"0xbd6100": 2,"0xb08b00": 3,"0x85961f": 4,
        "0x539f31": 5,"0xa9c8e" : 6,"0x7abd"  : 7,"0x303ff" : 8,
        "0x2f52a2": 9,"0x624bad":10,"0x7b7b7b":11,"0x3c3c3c":12,
        "0xff0505":13,"0xbfba69":14,"0xa6be00":15,"0x7ac634":16,
        "0x3dc300":17,"0xbfaf"  :18,"0x10a4ee":19,"0x5480e4":20,
        "0x886ce4":21,"0xa34bad":22,"0xb73d69":23,"0x965735":24,
        "0xf66c03":25,"0xbffb00":26,"0x87ff67":27,"0x1aff2f":28,
        "0x25ffa8":29,"0x4dffd2":30,"0x19e9ff":31,"0x8bc5ff":32,
        "0x92a7ff":33,"0xb88dff":34,"0xd86ce4":35,"0xff39d4":36,
        "0xffa529":37,"0xfff034":38,"0xe3f403":39,"0xdbc300":40,
        "0xbe9d63":41,"0x89b47d":42,"0x88c2ba":43,"0x9bb3c4":44,
        "0x85a5c2":45,"0xc68b7c":46,"0xf14080":47,"0xff94a6":48,
        "0xffa374":49,"0xffee9f":50,"0xd2e498":51,"0xbad074":52,
        "0xa9a9a9":53,"0xd4fde1":54,"0xcdf1f8":55,"0xb9c1e3":56,
        "0xcdbbe4":57,"0xd0d0d0":58,"0xdfe6e5":59,"0xffffff":60
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
