# ESP32 Tracking System  

Acelerômetro (MPU6050) • GPS (GY-GPS6MU2) • LoRa SX1276/SX1278 • Sensor de Luminosidade (LDR/TSL2561)

Este projeto utiliza um **ESP32** integrado a vários sensores para coleta e transmissão de dados em tempo real:

- 📍 **GPS GY-GPS6MU2 (u-blox NEO-6M)**
- 📐 **Acelerômetro/Giroscópio MPU6050**
- 📡 **Módulo LoRa SX1276/1278 (433/868/915 MHz)**
- ☀️ **Sensor de luminosidade (LDR ou TSL2561)**
- 🧠 Envio dos dados via Serial, LoRa ou WiFi (dependendo da sua configuração)

Este README ensina o passo a passo para **clonar o repositório**, instalar os **drivers**, configurar o **ESP32** e colocar tudo para funcionar.

---

## 📦 Requisitos do Sistema

**Hardware**

- ESP32 DevKit V1 (ou equivalente)
- Módulo GPS GY-GPS6MU2 (u-blox NEO-6M)
- Módulo MPU6050
- Módulo LoRa SX1276/SX1278
- LDR + resistor 10k **ou** TSL2561 (digital)
- Jumpers e protoboard

**Software**

- Arduino IDE (versão 1.8.x ou 2.x)
- Drivers USB CP210X ou CH340 (verifique seu ESP32)
- Git instalado

---

## 🔌 Instalando o Driver do ESP32

Existem dois chips USB comuns no ESP32:

- **CP2102** (mais comum):  
  [Baixar driver](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
- **CH340** (modelos mais baratos):  
  [Baixar driver](https://sparks.gogo.co.nz/ch340.html)

<details>
<summary><strong>Como saber qual você precisa?</strong></summary>

1. Conecte o ESP32 ao PC.
2. Abra o <em>Gerenciador de Dispositivos</em> (Windows).
3. Em <em>Portas (COM & LPT)</em>, verifique o nome apresentado:
   - "CP210x USB to UART Bridge" → driver CP2102
   - "USB-SERIAL CH340" → driver CH340
   - Se mostrar COM detectado corretamente, o driver já está instalado.
</details>

---

## 🛠 Instalando Suporte ESP32 na Arduino IDE

1. Abra a Arduino IDE, vá em **File → Preferences**.
2. Em **Additional Boards Manager URLs**, adicione:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Vá em **Tools > Board > Boards Manager**.
4. Pesquise por **ESP32** e clique em <ins>Install</ins>.
5. Selecione a placa: **Tools > Board > ESP32 Arduino > ESP32 Dev Module**

---

## 📥 Clonando o Repositório

1. Instale o Git: [Download](https://git-scm.com/downloads)
2. No terminal:
   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
   ```

---

## 📚 Instalando Bibliotecas Necessárias

No menu da Arduino IDE, vá em: **Sketch > Include Library > Manage Libraries**

Instale as bibliotecas:

- <strong>Adafruit MPU6050</strong>
- <strong>Adafruit Unified Sensor</strong>
- <strong>Adafruit BusIO</strong>
- <strong>TinyGPS++</strong>
- <strong>LoRa (por Sandeep Mistry)</strong>
- <strong>Adafruit TSL2561</strong> (se for sensor digital)
- LDR comum não precisa de biblioteca

---

## ⚡ Ligações dos Sensores ao ESP32

### MPU6050 (I2C)
| MPU6050 | ESP32   |
| ------- | ------- |
| VCC     | 3.3V    |
| GND     | GND     |
| SCL     | GPIO 22 |
| SDA     | GPIO 21 |

### GPS GY-GPS6MU2 (UART)
| GPS | ESP32         |
| --- | ------------- |
| VCC | 5V            |
| GND | GND           |
| TX  | GPIO 16 (RX2) |
| RX  | GPIO 17 (TX2) |

> O módulo NEO-6M usa 9600 baud por padrão.

### LoRa SX1276/SX1278 (SPI)
| LoRa   | ESP32    |
| ------ | -------- |
| VCC    | 3.3V     |
| GND    | GND      |
| SCK    | GPIO 18  |
| MISO   | GPIO 19  |
| MOSI   | GPIO 23  |
| NSS/CS | GPIO 5   |
| RST    | GPIO 14  |
| DIO0   | GPIO 2   |

### Sensor de Luminosidade

<strong>Opção A — LDR (analógico):</strong>  
• Uma perna do LDR vai no 3.3V, a outra no GPIO 34 e resistor de 10k para GND.  
• O ponto entre o LDR e o resistor vai para a entrada analógica (GPIO 34).

<strong>Opção B — TSL2561 (I2C):</strong>
| TSL2561 | ESP32   |
| ------- | ------- |
| VIN     | 3.3V    |
| GND     | GND     |
| SCL     | GPIO 22 |
| SDA     | GPIO 21 |

---

## ▶️ Enviando o Código para o ESP32

1. Conecte o ESP32 no computador.  
2. Selecione em **Tools > Board > ESP32 Dev Module**.  
3. Escolha a porta: **Tools > Port > COMX**
4. Clique em <ins>Upload</ins>.

> **Erro comum:**  
> “Failed to connect to ESP32: Timeout waiting for packet header”  
> **Solução:** Segure o botão BOOT por 1–2 segundos quando o upload começar.

---

## 🔎 Lendo os Dados via Serial

Na Arduino IDE, abra **Tools > Serial Monitor** e selecione **115200 baud**.

**Exemplo de saída:**
```
GPS: -5.04143, -42.47396, 0.7 m/s
ACC: 0.10, 9.82, 0.40
GYRO: 0.02, -0.01, 0.03
Luminosidade: 264
LoRa: pacote enviado
```
