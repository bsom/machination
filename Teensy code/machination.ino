#include <Wire.h>
#include <i2cEncoderLibV2.h>

// constants
const int IntPin = 17; //Interrupt Pin
#define ENCODER_N 8 //Number of encoders
const unsigned long colorTable[] = {0xed4325,0xbd6100,0xb08b00,
        0x85961f,0x539f31,0x0a9c8e,0x007abd,0x0303ff,0x2f52a2,
        0x624bad,0x7b7b7b,0x3c3c3c,0xff0505,0xbfba69,0xa6be00,
        0x7ac634,0x3dc300,0x00bfaf,0x10a4ee,0x5480e4,0x886ce4,
        0xa34bad,0xb73d69,0x965735,0xf66c03,0xbffb00,0x87ff67,
        0x1aff2f,0x25ffa8,0x4dffd2,0x19e9ff,0x8bc5ff,0x92a7ff,
        0xb88dff,0xd86ce4,0xff39d4,0xffa529,0xfff034,0xe3f403,
        0xdbc300,0xbe9d63,0x89b47d,0x88c2ba,0x9bb3c4,0x85a5c2,
        0xc68b7c,0xf14080,0xff94a6,0xffa374,0xffee9f,0xd2e498,
        0xbad074,0xa9a9a9,0xd4fde1,0xcdf1f8,0xb9c1e3,0xcdbbe4,
        0xd0d0d0,0xdfe6e5,0xffffff,0x191919};

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
