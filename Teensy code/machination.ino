#include <Wire.h>
#include <i2cEncoderLibV2.h>

// constants
const int IntPin = 17; //Interrupt Pin
#define ENCODER_N 8 //Number of encoders
const unsigned long colorTable[] = {0xee97a5,0xf0a648,0xc29841,0xf7f28a,0xccf84e,0x7dfa57,0x7efaad,
                                    0x8ffbe7,0x96c3fa,0x5d80dc,0x94a6f9,0xc773dd,0xd15e9c,0xffffff,
                                    0xe84a42,0xe27230,0x917251,0xfdee5c,0xa7fb7a,0x6abe3a,0x5abbad,
                                    0x70e5fc,0x4ea1e7,0x3a7bb9,0x816fdc,0xaa7ac0,0xe750cd,0xcfcfcf,
                                    0xd06d5f,0xf0a47b,0xcbac78,0xf0fdb5,0xd5e29e,0xbdcd7d,0xa3c190,
                                    0xdcfbe2,0xd3f0f7,0xb9c0df,0xc8bbe0,0xa899df,0xe2dbe0,0xa7a7a7,
                                    0xbc928b,0xad825c,0x93826c,0xbdb872,0xaaba3c,0x88ac5a,0x94bfb8,
                                    0x9eb1c1,0x8aa3be,0x8492c6,0xa094b1,0xb79fba,0xaf7493,0x7a7a7a,
                                    0x9e3e3a,0x9b553b,0x6c5145,0xd6c140,0x879339,0x689b43,0x4b988c,
                                    0x396280,0x23358f,0x39549b,0x5d4fa6,0x9553a6,0xb83f6d,0x3e3e3e,
                                    };

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
