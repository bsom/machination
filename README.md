# Machination

## This project is unproven as of yet.  Wait for the 1.0 release before attempting to replicate this project!

Plot to create a hodge-podge Eurorack laptop-like PC with a simple embedded MIDI control surface.

This project was designed for my use but I figure that someone else out there might find it interesting as well.

The Teensy-based MIDI controller code here is designed for a workflow that I use with Ableton Live.  Instead of the encoders sending MIDI CC, they send MIDI notes, each encoder on its own MIDI channel.  The encoders select all MIDI notes from 0-127 and wrap back around when they overflow past 127 or below 0, sending the notes in a stream on MIDI channels 9-16.  When the encoder is pushed, it sends the currently selected note on MIDI channels 1-8.  This is a fast way for me to improvise using 100's of small clips in Ableton Live.

- [x] Identify hardware to use
- [x] Identify cabling to use
- [ ] Figure out how to mount Teensy (double-sided tape? carrier board?)
- [x] Find power solution to power both display and NUC
- [x] Figure out front panel footprint for USB header cable
- [x] Program Teensy to read encoders and output MIDI to PC via USB
- [X] Configure AMOLED display in Windows (resolution, zoom, orientation)
- [ ] Design front panel with standoffs for display and NUC
- [ ] Order front panel from Front Panel Express
- [ ] Experiment with full screen Python application for easier display versus tiny Ableton Live screen (Kivy?)
- [ ] Create a virtual MIDI port to split MIDI from Teensy to Ableton and Python using LoopBe1 and MIDI Patchbay
  * http://en.soundigy.com/midipatchbay.php
  * https://www.nerds.de/en/loopbe1.html
