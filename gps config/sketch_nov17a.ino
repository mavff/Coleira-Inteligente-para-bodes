#include <HardwareSerial.h>

HardwareSerial GPS(2);

const uint8_t ubxRate5Hz[] = {
  0xB5, 0x62, 0x06, 0x08, 0x06, 0x00,
  0xC8, 0x00, 0x01, 0x00, 0x01, 0x00,
  0xDD, 0x68
};

void sendUBX(const uint8_t *msg, uint8_t len) {
  for (int i = 0; i < len; i++) GPS.write(msg[i]);
}

void setup() {
  Serial.begin(115200);

  GPS.begin(9600, SERIAL_8N1, 16, 17);
  delay(1000);

  Serial.println("Configurando GPS...");

  // Exemplo: colocar GPS a 5Hz
  sendUBX(ubxRate5Hz, sizeof(ubxRate5Hz));
  delay(200);

  Serial.println("GPS pronto.\n");
}

void loop() {
  while (GPS.available()) {
    String linha = GPS.readStringUntil('\n');
    Serial.println(linha);
  }
}
