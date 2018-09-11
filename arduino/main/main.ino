#include <SPI.h>
#include <RFID.h>

RFID RFID(10, 9);

int UID[5];

void setup()
{
  Serial.begin(9600);
  SPI.begin();
  RFID.init();
}

void loop()
{
  if (RFID.isCard()) {
    if (RFID.readCardSerial()) {
      for (int i = 0; i < 5; i++) {
        UID[i] = RFID.serNum[i];
        Serial.print(UID[i], DEC);
      }
    }
    RFID.halt();
  }
  delay(500);
}
