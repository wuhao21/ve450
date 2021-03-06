This zip file contains firmware and libraries designed to run on an Arduino, or Arduino clone. It contains all the files you should need to get everything up and running, as well as some test firmware to let you test various parts of your system.

All documentation on the electronics themselves are located at http://make.rrrf.org/electronics-2.0


####### Please build this project and burn it onto an Arduino Uno
/gcode/GCode_Interpreter

this firmware receives and parses GCode commands over serial.  pretty rad.



Here is an explanation of the various files contained:

/library

all the folders contained in this directory need to be copied into the library folder of your Arduino installation.  on Arduino 10, this is arduino-0010/hardware/libraries.

/snap

these are the firmwares that you would actually upload to the Arduino itself.  each folder is a 'sketch' that you open with the Arduino software and load onto your board.  the top of each file contains pin definitions that will help you hook up your electronics to your Arduino.

/gcode

this folder contains some experimental software that implements GCode on the Arduino!


/gcode/GCode_Interpreter_Experimental

this is an experimental gcode based firmware with support for a rotary encoder on the extruder

/snap/3Axis_SNAP

this is the firmware that controls 3 stepper motors + limit switches on one Arduino.  this is for 2 arduino setups where one firmware controls the cartesian bot and the other controls the extruder(s)

/snap/Extruder_SNAP

this is the firmware that controls a Thermoplastic Extruder.  this is the corresponding firmware for a 2 arduino setup.

/snap/Single_Arduino_SNAP

this is the firmware that controls both the Cartesian Bot (3 steppers + limit switches) as well as a Thermoplastic Extruder.  This is the firmware you use for a single Arduino setup.  its pretty much maxed out.
