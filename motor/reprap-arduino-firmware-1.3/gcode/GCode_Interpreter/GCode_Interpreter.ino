// Arduino G-code Interpreter
// v1.0 by Mike Ellery - initial software (mellery@gmail.com)
// v1.1 by Zach Hoeken - cleaned up and did lots of tweaks (hoeken@gmail.com)
// v1.2 by Chris Meighan - cleanup / G2&G3 support (cmeighan@gmail.com)
// v1.3 by Zach Hoeken - added thermocouple support and multi-sample temp readings. (hoeken@gmail.com)
#include <HardwareSerial.h>
#define SIG_START 8

//our command string
#define COMMAND_SIZE 128
char comm[COMMAND_SIZE];
byte serial_count;
int no_data = 0;

void setup()
{
	//Do startup stuff here
	Serial.begin(19200);
	Serial.println("start");
	
	//other initialization.
	init_process_string();
	init_steppers();
	init_extruder();

  // Process On signal
  pinMode(SIG_START, OUTPUT);
  digitalWrite(SIG_START, LOW);
}

void loop()
{
	char c;
	
	//keep it hot!
	extruder_manage_temperature();

	//read in characters if we got them.
	if (Serial.available() > 0)
	{
		c = Serial.read();
		no_data = 0;
		
		//newlines are ends of commands.
		if (c != '\n')
		{
			comm[serial_count] = c;
			serial_count++;
		}
	}
	//mark no data.
	else
	{
		no_data++;
		delayMicroseconds(100);
	}

	//if theres a pause or we got a real command, do it
	if (serial_count && (c == '\n' || no_data > 100))
	{
		//process our command!
    digitalWrite(SIG_START, HIGH);
		process_string(comm, serial_count);
    digitalWrite(SIG_START, LOW);
		//clear command.
		init_process_string();
	}

	//no data?  turn off steppers
	if (no_data > 1000)
	  disable_steppers();
}
