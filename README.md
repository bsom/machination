# Machination

![alt text](https://github.com/bsom/machination/blob/master/images/panelv4.1.png?raw=true)


## This project is unproven as of yet.  Wait for the 1.0 release before attempting to replicate this project!

Current Progress: ███████████████████████████████████████████░░░░░░░ 89%

#### Check the WIKI for building instructions (which are still under construction, but progressing nicely!)

Plot to create a hodge-podge Eurorack laptop-like PC with a simple embedded MIDI control surface.  The idea was to use off-the-shelf parts as much as possible.  There is only one 'custom' internal piece that needs to be laser cut.  Everything else internal is readily available online.

This project was designed for my use but I figure that someone else out there might find it interesting as well.

The Teensy-based MIDI controller code here is designed for a workflow that I use with Ableton Live.  Instead of the encoders sending MIDI CC, they send MIDI notes, each encoder on its own MIDI channel.  The encoders select all MIDI notes from 0-127 and wrap back around when they overflow past 127 or below 0, sending the notes in a stream on MIDI channels 9-16 to my Python script to update the on-screen display.  When the encoder is pushed, it sends the currently selected note on MIDI channels 1-8 instead.  The Python script passes these values (Channels 1-8 only) onto Ableton Live to trigger loops. This is a fast way for me to improvise using 100's of small clips in Ableton Live.

Things that need to be done:

- [x] Identify hardware to use
- [x] Identify cabling to use
- [x] Figure out how to mount Teensy (Seems like double-sided tape wins)
- [x] Find power solution to power both display and NUC
- [x] Figure out front panel footprint for USB header cable
- [x] Program Teensy to read encoders and output MIDI to PC via USB
- [X] Configure AMOLED display in Windows (resolution, zoom, orientation)
- [x] Design front panel with standoffs for display and NUC
- [x] Order test front panel from Front Panel Express
- [x] Order FINAL front panel from Front Panel Express
- [ ] Write full screen Python application for easier display/interaction versus tiny Ableton Live screen, using [Kivy](https://kivy.org/) and [AbletonOSC](https://github.com/ideoforms/AbletonOSC)
