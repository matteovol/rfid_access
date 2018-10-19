#include <SPI.h>
#include <RFID.h>
#include "pitches.h"

RFID RFID(10, 9);
int UID[5];
const int LED = 6;
int noteDurations[] = {8, 8};
int melody[] = {NOTE_C4, NOTE_G3};
/* int noteDurations[] = {4, 8, 8, 4, 4, 4, 4, 4}; */
/* int melody[] = {NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4}; */

void setup()
{
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
  SPI.begin();
  RFID.init();
}

void loop()
{
  if (RFID.isCard()) {
    if (RFID.readCardSerial()) {
      digitalWrite (LED, HIGH);
      for (int i = 0; i < 5; i++) {
        UID[i] = RFID.serNum[i];
        Serial.print(UID[i], DEC);
      }
      for (int thisNote = 0; thisNote < 2; thisNote++) {
        int noteDuration = 1000 / noteDurations[thisNote];
        tone(8, melody[thisNote], noteDuration);

        int pauseBetweenNotes = noteDuration * 1.30;
        delay(pauseBetweenNotes);
        noTone(8);
        delay(50);
      }
    }
    digitalWrite (LED, LOW);
  }
  RFID.halt();
  delay(500);
}
