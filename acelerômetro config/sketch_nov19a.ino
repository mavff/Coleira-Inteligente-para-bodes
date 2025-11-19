#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// Cria um objeto para o sensor
Adafruit_MPU6050 mpu;

void setup() {
  // Inicia a serial para vermos os dados no PC
  Serial.begin(115200); 

  Serial.println("Tentando encontrar o MPU6050...");

  // Tenta iniciar o MPU6050
  if (!mpu.begin()) {
    Serial.println("Falha ao encontrar o MPU6050. Verifique a fiação!");
    // Trava aqui se não encontrar
    while (1) {
      delay(10);
    }
  }

  Serial.println("MPU6050 Encontrado!");

  // (Opcional) Configura as faixas de medição
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G); // +- 8G
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);      // +- 500 graus/s
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);    // Filtro
}

void loop() {
  // Cria "eventos" (pacotes de dados)
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Imprime os dados do Acelerômetro (em m/s^2)
  Serial.print("Acel X: ");
  Serial.print(a.acceleration.x);
  Serial.print(", Y: ");
  Serial.print(a.acceleration.y);
  Serial.print(", Z: ");
  Serial.print(a.acceleration.z);
  Serial.println(" m/s^2");

  // Imprime os dados do Giroscópio (em rad/s)
  Serial.print("Giro X: ");
  Serial.print(g.gyro.x);
  Serial.print(", Y: ");
  Serial.print(g.gyro.y);
  Serial.print(", Z: ");
  Serial.print(g.gyro.z);
  Serial.println(" rad/s");

  // Imprime a Temperatura (em °C)
  Serial.print("Temp: ");
  Serial.print(temp.temperature);
  Serial.println(" *C");

  Serial.println("--------------------------------");
  
  delay(500); // Meio segundo de espera
}