#include <Wire.h>
#include <i2cEncoderLibV2.h>

// constants
const int IntPin = 17; //Interrupt Pin
#define ENCODER_N 8 //Number of encoders
const unsigned long colorTable[] = {0xff94a6,0xffa529,0xcc9927,0xf7f47c,0xbffb00,0x1aff2f,0x25ffa8,
                                    0x5cffe8,0x8bc5ff,0x5480e4,0x92a7ff,0xd86ce4,0xe553a0,0xffffff,
                                    0xff3636,0xf66c03,0x99724b,0xfff034,0x87ff67,0x3dc300,0xbfaf  ,
                                    0x19e9ff,0x10a4ee,0x7dc0  ,0x886ce4,0xb677c6,0xff39d4,0xd0d0d0,
                                    0xe2675a,0xffa374,0xd3ad71,0xedffae,0xd2e498,0xbad074,0x9bc48d,
                                    0xd4fde1,0xcdf1f8,0xb9c1e3,0xcdbbe4,0xae98e5,0xe5dce1,0xa9a9a9,
                                    0xc6928b,0xb78256,0x99836a,0xbfba69,0xa6be00,0x7db04d,0x88c2ba,
                                    0x9bb3c4,0x85a5c2,0x8393cc,0xa595b5,0xbf9fbe,0xbc7196,0x7b7b7b,
                                    0xaf3333,0xa95131,0x724f41,0xdbc300,0x85961f,0x539f31,0xa9c8e ,
                                    0x236384,0x1a2f96,0x2f52a2,0x624bad,0xa34bad,0xcc2e6e,0x3c3c3c};

i2cEncoderLibV2 Encoder();
//Class initialization with the I2C addresses
i2cEncoderLibV2 RGBEncoder[ENCODER_N] = { i2cEncoderLibV2(0b0000001), i2cEncoderLibV2(0b0000010), i2cEncoderLibV2(0b0000011), i2cEncoderLibV2(0b0000100),
                                          i2cEncoderLibV2(0b0000101), i2cEncoderLibV2(0b0000110), i2cEncoderLibV2(0b0000111), i2cEncoderLibV2(0b0001000)
                                        };

uint8_t encoder_status, i;

void encoder_rotated(i2cEncoderLibV2* obj) {
  if (obj->readStatus(i2cEncoderLibV2::RINC)){
    //Serial.print("Increment \n");
    }
  else{
    //Serial.print("Decrement \n");
    }
    
  usbMIDI.sendNoteOn(obj->readCounterInt(),127,(obj->id)+9);
  //Serial.print(obj->id);
  //Serial.print(": ");
  //Serial.println(obj->readCounterInt());
  
}

void encoder_click(i2cEncoderLibV2* obj) {
  Serial.print("Push: ");
  Serial.println(obj->id);
  usbMIDI.sendNoteOn(obj->readCounterInt(),127,(obj->id)+1);
}


void encoder_thresholds(i2cEncoderLibV2* obj) {
  //if (!(obj->readStatus(i2cEncoderLibV2::RMAX)))
  //obj->writeRGBCode(0xFF0000);
}

void encoder_fade(i2cEncoderLibV2* obj) {
  obj->writeRGBCode(0x000000);
}

void onCC(byte channel, byte control, byte value){
      Serial.print(int(channel));
      Serial.print("\n");
      Serial.print(int(control));
      Serial.print("\n");
      Serial.print(int(value));
      Serial.print("\n\n");
      RGBEncoder[channel-1].writeRGBCode(colorTable[value-1]);
}


void setup() {
  uint8_t enc_cnt;

  //start i2c library
  Wire.begin();

  usbMIDI.setHandleControlChange(onCC);
  
  //Reset all of the encoders
  for (enc_cnt = 0; enc_cnt < ENCODER_N; enc_cnt++) {
    RGBEncoder[enc_cnt].reset();
  }

  //config interrupt pin
  pinMode(IntPin, INPUT);

  //debug LED
  pinMode(13,OUTPUT);

  // Initialize the encoders
  for (enc_cnt = 0; enc_cnt < ENCODER_N; enc_cnt++) {
    RGBEncoder[enc_cnt].begin(
      i2cEncoderLibV2::INT_DATA | i2cEncoderLibV2::WRAP_ENABLE
      | i2cEncoderLibV2::DIRE_RIGHT
      | i2cEncoderLibV2::IPUP_ENABLE
      | i2cEncoderLibV2::RMOD_X1
      | i2cEncoderLibV2::RGB_ENCODER);
    RGBEncoder[enc_cnt].writeCounter((int32_t) 0); //Reset of the CVAL register
    RGBEncoder[enc_cnt].writeMax((int32_t) 127); //Set the maximum threshold to 127
    RGBEncoder[enc_cnt].writeMin((int32_t) 0); //Set the minimum threshold to 0
    RGBEncoder[enc_cnt].writeStep((int32_t) 1); //The step at every encoder click is 1
    RGBEncoder[enc_cnt].writeRGBCode(0x191919); 
    RGBEncoder[enc_cnt].writeAntibouncingPeriod(35); //350ms of debouncing

    // encoder events
    RGBEncoder[enc_cnt].onChange = encoder_rotated;
    RGBEncoder[enc_cnt].onButtonPush = encoder_click;
    RGBEncoder[enc_cnt].onMinMax = encoder_thresholds;
    RGBEncoder[enc_cnt].onFadeProcess = encoder_fade;

    // Enable the I2C Encoder V2 interrupts
    RGBEncoder[enc_cnt].autoconfigInterrupt();
    RGBEncoder[enc_cnt].id = enc_cnt;


    //Blink after configuration of encoder as LED/config test
    RGBEncoder[enc_cnt].writeFadeRGB(0);
    RGBEncoder[enc_cnt].writeRGBCode(0xFF0000);
    delay(90);
    RGBEncoder[enc_cnt].writeRGBCode(0x00FF00);
    delay(90);
    RGBEncoder[enc_cnt].writeRGBCode(0x0000FF);
    delay(90);
    RGBEncoder[enc_cnt].writeRGBCode(0x191919);
    delay(90);
  }
}

void loop() {

  usbMIDI.read();
  uint8_t enc_cnt;
  
  if (digitalRead(IntPin) == LOW) {
    //Interrupt from the encoders, start to scan the encoder matrix
    for (enc_cnt = 0; enc_cnt < ENCODER_N; enc_cnt++) {
      if (digitalRead(IntPin) == HIGH) { //If the interrupt pin return high, exit from the encoder scan
        break;
      }
      RGBEncoder[enc_cnt].updateStatus();
    }
  }

  }
