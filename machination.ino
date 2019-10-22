#include <Wire.h>
#include <i2cEncoderLibV2.h>

// constants
const int IntPin = 17; //Interrupt Pin
#define ENCODER_N 8 //Number of encoders

i2cEncoderLibV2 Encoder();
//Class initialization with the I2C addresses
i2cEncoderLibV2 RGBEncoder[ENCODER_N] = { i2cEncoderLibV2(0b0000001), i2cEncoderLibV2(0b0000010), i2cEncoderLibV2(0b0000011), i2cEncoderLibV2(0b0000100),
                                          i2cEncoderLibV2(0b0000101), i2cEncoderLibV2(0b0000110), i2cEncoderLibV2(0b1000111), i2cEncoderLibV2(0b0001000)
                                        };

uint8_t encoder_status, i;

void encoder_rotated(i2cEncoderLibV2* obj) {
  if (obj->readStatus(i2cEncoderLibV2::RINC))
    Serial.print("Increment ");
  else
    Serial.print("Decrement ");
  Serial.print(obj->id);
  Serial.print(": ");
  Serial.println(obj->readCounterInt());
  obj->writeRGBCode(0x00FF00);
}

void encoder_click(i2cEncoderLibV2* obj) {
  Serial.print("Push: ");
  Serial.println(obj->id);
  obj->writeRGBCode(0x0000FF);
}

void encoder_thresholds(i2cEncoderLibV2* obj) {
  if (obj->readStatus(i2cEncoderLibV2::RMAX))
    Serial.print("Max: ");
  else
    Serial.print("Min: ");
  Serial.println(obj->id);
  obj->writeRGBCode(0xFF0000);
}

void setup() {
  uint8_t enc_cnt;

  //start i2c library
  Wire.begin();
  
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
    RGBEncoder[enc_cnt].writeRGBCode(0x000000); //Turn off LEDs
    RGBEncoder[enc_cnt].writeAntibouncingPeriod(20); //200ms of debouncing

    // encoder events
    RGBEncoder[enc_cnt].onChange = encoder_rotated;
    RGBEncoder[enc_cnt].onButtonPush = encoder_click;
    RGBEncoder[enc_cnt].onMinMax = encoder_thresholds;

    // Enable the I2C Encoder V2 interrupts
    RGBEncoder[enc_cnt].autoconfigInterrupt();
    RGBEncoder[enc_cnt].id = enc_cnt;

    //Blink after configuration of encoder as LED/config test
    RGBEncoder[enc_cnt].writeRGBCode(0xFF0000);
    delay(20);
    RGBEncoder[enc_cnt].writeRGBCode(0x00FF00);
    delay(20);
    RGBEncoder[enc_cnt].writeRGBCode(0x0000FF);
    delay(20);
    RGBEncoder[enc_cnt].writeRGBCode(0xFFFFFF);
    delay(20);
    RGBEncoder[enc_cnt].writeRGBCode(0x000000);
    digitalWrite(13,HIGH);
    delay(10);
    digitalWrite(13,LOW);
  }
}

void loop() {
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
  while (usbMIDI.read()) {
    // ignore incoming messages
  }
}
