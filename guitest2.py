import sys

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
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


Builder.load_string('''
<mainWindow>:
    orientation: 'horizontal'
    cols: 4
    rows: 2
    GridLayout:
        orientation: 'horizontal'
        cols: 4
        rows: 2
        Button:
            id: button1
            text: root.button1Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button1Color
            color: 255,255,255,1
        Button:
            id: button2
            text: root.button2Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button2Color
            color: 255,255,255,1
        Button:
            id: button3
            text: root.button3Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button3Color
            color: 255,255,255,1
        Button:
            id: button4
            text: root.button4Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button4Color
            color: 255,255,255,1
        Button:
            id: button5
            text: root.button5Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button5Color
            color: 255,255,255,1
        Button:
            id: button6
            text: root.button6Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button6Color
            color: 255,255,255,1
        Button:
            id: button7
            text: root.button7Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button7Color
            color: 255,255,255,1
        Button:
            id: button8
            text: root.button8Text
            font_size: 60
            halign: 'center'
            background_normal: ''
            background_color: root.button8Color
            color: 255,255,255,1
''')

from rtmidi.midiutil import open_midiinput
from func_timeout import func_timeout, FunctionTimedOut

clips = []
for j in range(8):
    column=[]
    for k in range(128):
        column.append("(empty)")
    clips.append(column)


def printOutput(address: str, *args: List[Any]) -> None:
    clips[args[0]][args[1]]=args[2]
    print(args[2])

def getclipname(server,client,track,clip):
    client.send_message("/live/name/clip",(track,clip))
    server.handle_request()

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

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port

    def __call__(self, event, data=None):
        MIDImessage, deltatime = event
        knob=MIDImessage[0]
        if knob > 151:
            value=MIDImessage[1]
            print("%r" % (MIDImessage))
            mainWindow.update_button(mainWindow,knob-151,value)
        else:
            value=MIDImessage[1]
            print("%r" % (MIDImessage))
            mainWindow.update_button(mainWindow,knob-143,value)
        

class mainWindow(GridLayout):
    button1Text = StringProperty('Encoder 1')
    button2Text = StringProperty('Encoder 2')
    button3Text = StringProperty('Encoder 3')
    button4Text = StringProperty('Encoder 4')
    button5Text = StringProperty('Encoder 5')
    button6Text = StringProperty('Encoder 6')
    button7Text = StringProperty('Encoder 7')
    button8Text = StringProperty('Encoder 8')
    button1Color = ColorProperty()
    button2Color = ColorProperty()
    button3Color = ColorProperty()
    button4Color = ColorProperty()
    button5Color = ColorProperty()
    button6Color = ColorProperty()
    button7Color = ColorProperty()
    button8Color = ColorProperty()

    def __init__(self, **kwargs):
        super(mainWindow, self).__init__(**kwargs)
        
    def update_button(self,knob,MIDImessage):
        buttonToChange = switch.get(knob)
        rootObj = App.get_running_app().root
        setattr(rootObj,buttonToChange+"Text", "Encoder " + str(knob) + "\nRaw: " + str(MIDImessage)+"\n"+str(clips[knob-1][MIDImessage]))
        setattr(rootObj,buttonToChange+"Color",(MIDImessage/127,(knob/16.0)+0.5,1.0-(MIDImessage/127),1))

class pyMachination(App):
    def build(self):
        #open MIDI port
        try:
            midiin, port_name = open_midiinput(0)
        except (EOFError, KeyboardInterrupt):
            sys.exit()

        #attach MIDI imput interrupt handler
        midiin.set_callback(MidiInputHandler(port_name))

        self.main_screen = mainWindow()

        dispatcher = Dispatcher()
        dispatcher.set_default_handler(printOutput)

        server = BlockingOSCUDPServer(("127.0.0.1", 9001),dispatcher)
        client = SimpleUDPClient("127.0.0.1", 9000)

        print("Getting clip names...")
        for track in range(8):
            print("Scanning Track " + str(track+1))
            for clip in range (128):
                try:
                    func_timeout(0.05,getclipname,args=(server,client,track,clip))
                except FunctionTimedOut:
                    continue
                

        return self.main_screen
        
        

if __name__ == '__main__':
    pyMachination().run()