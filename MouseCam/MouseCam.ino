#define SDIO 3
#define SCLK 2

#define DLEDG 9
#define DLEDR 10
#define DLEDY 11
#define DLEDPERF 13

#define FRAMELENGTH 324
byte frame[FRAMELENGTH];

byte flop;

void setup()
{
  pinMode(SCLK, OUTPUT);
  pinMode(SDIO, OUTPUT); 

  pinMode(DLEDY, OUTPUT);
  pinMode(DLEDR, OUTPUT);
  pinMode(DLEDG, OUTPUT);
  pinMode(DLEDPERF, OUTPUT);

  flash(DLEDY, 1);
  flash(DLEDR, 1);
  flash(DLEDG, 1);
  flash(DLEDPERF, 1);

  flop = false;

  Serial.begin(115200);
  Serial.println("Serial established.");
  Serial.flush();

  mouseInit();
  dumpDiag();
}

void loop()
{
  unsigned int s;
  int input;  

  readFrame(frame);

  //if( Serial.available() )
  //{
    input = 'd';
    switch( input )
    {
    case 'f': //if I recieve character f on serial, caputre a frame
      Serial.println("Frame capture.");
      readFrame(frame);
      Serial.println("Done.");
      break;
    case 'd': //
      for( input = 0; input < FRAMELENGTH; input++ )  //Reusing 'input' here
        Serial.write( frame[input] ); //write out the data
        
      Serial.write( 127 ); //add a space
      break;
    case 'y':
         Serial.write(readRegister(0x02));
         
      break;
    }
    Serial.flush();
  //}
}

void flash(byte pin, byte nTimes)
{
  while( nTimes-- )
  {
    digitalWrite(pin, HIGH);
    delay(120);
    digitalWrite(pin, LOW);
    delay(80);
  } 
}

void flipLED(void)
{
  flop = !flop;
  digitalWrite(DLEDY, flop ? HIGH : LOW);
}



/*  
 Serial driver for ADNS2010, by Conor Peterson (robotrobot@gmail.com)
 Serial I/O routines adapted from Martjin The and Beno?t Rosseau's work.
 Delay timings verified against ADNS2061 datasheet.
 
 The serial I/O routines are apparently the same across several Avago chips.
 It would be a good idea to reimplement this code in C++. The primary difference
 between, say, the ADNS2610 and the ADNS2051 are the schemes they use to dump the data
 (the ADNS2610 has an 18x18 framebuffer which can't be directly addressed).
 
 This code assumes SCLK is defined elsewhere to point to the ADNS's serial clock,
 with SDIO pointing to the data pin.
*/

//these bytes are addresses for data in the sensor's register
const byte regConfig    = 0x00; //write to this to reset the sensor, power down, or set "forced awake mode"
const byte regStatus    = 0x01; //read only: gives the mouse's id number (always 0) and whether the mouse is awake
const byte regPixelData = 0x08; //read the mouse's actual pixel data
const byte deltaY       = 0x02; //read only: change in y position
const byte deltaX       = 0x03; //read only: change in y position

//these bytes are data which can be written to the registers for requests
const byte maskNoSleep  = 0x01; //write to the regConfig address to set the "forced awake" mode
const byte maskPID      = 0xE0;


void mouseInit(void)
{
  digitalWrite(SCLK, HIGH); // pulse the clock signal (why?)
  delayMicroseconds(5);
  digitalWrite(SCLK, LOW);
  delayMicroseconds(1); //why is this delay less than the previous?
  digitalWrite(SCLK, HIGH);
  delay(1025);
  writeRegister(regConfig, maskNoSleep); //Force the mouse to be always on.
}

void dumpDiag(void)
{
  unsigned int val;

  val = readRegister(regStatus);

  Serial.print("Product ID: ");
  Serial.println( (unsigned int)((val & maskPID) >> 5));
  Serial.println("Ready.");
  Serial.flush();
}

void writeRegister(byte addr, byte data) //function to write data to the sensor's register
{
  byte i;

  addr |= 0x80; //Setting MSB high indicates a write operation. (change the first bit to 1 so that it's a write operation)

  //Write the address
  pinMode (SDIO, OUTPUT);
  for (i = 8; i != 0; i--)
  {
    digitalWrite (SCLK, LOW);
    digitalWrite (SDIO, addr & (1 << (i-1) ));
    digitalWrite (SCLK, HIGH);
  }

  //Write the data    
  for (i = 8; i != 0; i--)
  {
    digitalWrite (SCLK, LOW);
    digitalWrite (SDIO, data & (1 << (i-1) ));
    digitalWrite (SCLK, HIGH);
  }
}

byte readRegister(byte addr)
{
  byte i;
  byte r = 0;

  //Write the address
  pinMode (SDIO, OUTPUT);
  for (i = 8; i != 0; i--)
  {
    digitalWrite (SCLK, LOW);
    digitalWrite (SDIO, addr & (1 << (i-1) ));
    digitalWrite (SCLK, HIGH);
  }

  pinMode (SDIO, INPUT);  //Switch the dataline from output to input
  delayMicroseconds(110);  //Wait (per the datasheet, the chip needs a minimum of 100 µsec to prepare the data)

  //Clock the data back in
  for (i = 8; i != 0; i--)
  {                             
    digitalWrite (SCLK, LOW);
    digitalWrite (SCLK, HIGH);
    r |= (digitalRead (SDIO) << (i-1) );
  }

  delayMicroseconds(110);  //Tailing delay guarantees >100 µsec before next transaction

  return r;
}


//ADNS2610 dumps a 324-byte array, so this function assumes arr points to a buffer of at least 324 bytes.
void readFrame(byte *arr)
{
  byte *pos;
  byte *uBound;
  unsigned long timeout;
  byte val;

  //Ask for a frame dump
  writeRegister(regPixelData, 0x2A);

  val = 0;
  pos = arr;
  uBound = arr + 325;

  timeout = millis() + 1000;

  //There are three terminating conditions from the following loop:
  //1. Receive the start-of-field indicator after reading in some data (Success!)
  //2. Pos overflows the upper bound of the array (Bad! Might happen if we miss the start-of-field marker for some reason.)
  //3. The loop runs for more than one second (Really bad! We're not talking to the chip properly.)
  while( millis() < timeout && pos < uBound)
  {
    val = readRegister(regPixelData);
    

    //Only bother with the next bit if the pixel data is valid.
    if( !(val & 64) )
      continue;

    //If we encounter a start-of-field indicator, and the cursor isn't at the first pixel,
    //then stop. ('Cause the last pixel was the end of the frame.)
    if( ( val & 128 ) 
      &&  ( pos != arr) )
      break;

    *pos = val & 63;
    pos++;
  }
}  
  int getDeltaY(){
    return (readRegister(deltaY));
  }
  
  int getDeltaX(){
    return (readRegister(deltaX));
  }
