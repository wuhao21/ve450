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

#define SET_HOME "G92"
#define GO_HOME "G28"
#define SET_MM "G21"
#define SET_ABS "G90"
#define DRAW_CIRC_LARGE "G2 X0 Y0 I50"
#define DRAW_CIRC_SMALL "G2 X50 Y50 I20"
#define GO_MID "G1 X50 Y50 F1500"
#define GO_END "G1 X100 Y100 F1500"

void P1()
{
 
}
void P2()
{}
void P3()
{}
void P4()
{}

void setup()
{
	//Do startup stuff here
	Serial.begin(19200);
	//Serial.println("start");
	
	//other initialization.
	init_process_string();
	init_steppers();
	init_extruder();

  // Process On signal
  pinMode(SIG_START, OUTPUT);
  digitalWrite(SIG_START, LOW);

  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);

  process_string("G21\n",4); //Set to MM unit
  delay(5000); // wait for 10 secs
  Serial.read(); // clear read buffer
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
		if (c != '\n' || c != 0)
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
    if(comm[0] == 'P')
    {
      switch(comm[1])
      {
         case '1':
             P1();
             break;
         case '2':
             P2();
             break;
         case '3':
             P3();
             break;
         case '4':
             P4();
       }
    }
    else if(comm[0] == 'S')
    {
      digitalWrite(SIG_START, HIGH);
      Serial.println("ok");
    }
    else if(comm[0] == 'E')
    {
      digitalWrite(SIG_START, LOW);
      Serial.println("ok");
    }
    else if(comm[0] == 'G')
    {
  		process_string(comm, serial_count);
    }
		//clear command.
		init_process_string();
	}

	//no data?  turn off steppers
	if (no_data > 1000)
	  disable_steppers();
}
