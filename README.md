# ESP32 Tracking System  
### Acelerômetro (MPU6050) • GPS (GY-GPS6MU2) • LoRa SX1276/SX1278 • Sensor de Luminosidade (LDR/TSL2561)

Este projeto utiliza um **ESP32** integrado a vários sensores para coleta e transmissão de dados em tempo real:

- 📍 **GPS GY-GPS6MU2 (u-blox NEO-6M)**
- 📐 **Acelerômetro/Giroscópio MPU6050**
- 📡 **Módulo LoRa SX1276/1278 (433/868/915 MHz)**
- ☀️ **Sensor de luminosidade (LDR ou TSL2561)**
- 🧠 Envio dos dados via Serial, LoRa ou WiFi (dependendo da sua configuração)

Este README ensina exatamente o que você precisa fazer para **clonar o repositório**, instalar os **drivers**, configurar o **ESP32**, e colocar tudo para funcionar.

---

# 📦 1. Requisitos do Sistema

### **Hardware**
- ESP32 DevKit V1 (ou modelo equivalente)
- Módulo GPS GY-GPS6MU2 (u-blox NEO-6M)
- Módulo MPU6050
- Módulo LoRa SX1276/SX1278
- LDR + resistor 10k **ou** TSL2561 (digital)
- Jumpers e protoboard

### **Software**
- Arduino IDE (versão 1.8.x ou 2.x)
- Drivers USB CP210X ou CH340 (dependendo do seu ESP32)
- Git instalado

---

# 🔌 2. Instalando o Driver do ESP32

Existem dois chips USB usados no ESP32:

### ✔ **CP2102 (mais comum)**
Driver:  
https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers

### ✔ **CH340 (modelos mais baratos)**
Driver:  
https://sparks.gogo.co.nz/ch340.html

### Como saber qual você precisa?
1. Conecte o ESP32 no PC.  
2. Abra o **Gerenciador de Dispositivos** (Windows).  
3. Vá em **Portas (COM & LPT)**.
4. Veja o nome:
   - **"CP210x USB to UART Bridge" → precisa do driver CP2102**
   - **"USB-SERIAL CH340" → precisa do driver CH340**
   - Se mostrar **COM detectado corretamente**, o driver já está instalado.

---

## 🛠 3. Instalando o Suporte ao ESP32 na Arduino IDE

Abra a Arduino IDE e vá em:

**File → Preferences**

Em **Additional Boards Manager URLs** coloque:

https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json



Depois:

1. Vá em **Tools → Board → Boards Manager**
2. Pesquise por **ESP32**
3. Clique em **Install**

Após a instalação, selecione a placa:

**Tools → Board → ESP32 Arduino → ESP32 Dev Module**

---

## 📥 4. Clonando o Repositório (Git)

Instale o Git se ainda não tiver:  
https://git-scm.com/downloads

Depois abra o terminal e execute:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO

## 📚 5. Instalando as Bibliotecas Necessárias

Abra o gerenciador de bibliotecas:

`Sketch → Include Library → Manage Libraries`

Instale as seguintes bibliotecas:

### 📐 Acelerômetro MPU6050
- **Adafruit MPU6050**
- **Adafruit Unified Sensor**
- **Adafruit BusIO**

### 📍 GPS GY-GPS6MU2 / NEO-6M
- **TinyGPS++**

### 📡 LoRa SX1276/SX1278
- **LoRa (por Sandeep Mistry)**

### ☀️ Sensor de Luminosidade
- **Adafruit TSL2561** (se for sensor digital)
- **LDR comum não precisa de biblioteca**

---

## ⚡ 6. Ligações dos Sensores ao ESP32

### 📐 MPU6050 (I2C)
| MPU6050 | ESP32 |
|--------|-------|
| VCC | 3.3V |
| GND | GND |
| SCL | GPIO **22** |
| SDA | GPIO **21** |

---

### 📍 GPS GY-GPS6MU2 (UART)
| GPS | ESP32 |
|------|--------|
| VCC | 5V |
| GND | GND |
| TX | GPIO **16** (RX2) |
| RX | GPIO **17** (TX2) |

> O módulo NEO-6M utiliza **9600 baud** por padrão.

---

### 📡 Módulo LoRa SX1276/SX1278 (SPI)
| LoRa | ESP32 |
|------|--------|
| VCC | 3.3V |
| GND | GND |
| SCK | GPIO **18** |
| MISO | GPIO **19** |
| MOSI | GPIO **23** |
| NSS / CS | GPIO **5** |
| RST | GPIO **14** |
| DIO0 | GPIO **2** |

---

### ☀️ Sensor de Luminosidade

#### **Opção A — LDR (analógico)**  
Montagem:

#### **Opção B — TSL2561 (I2C)**
| TSL2561 | ESP32 |
|--------|--------|
| VIN | 3.3V |
| GND | GND |
| SCL | GPIO **22** |
| SDA | GPIO **21** |

---

## ▶️ 7. Enviando o Código para o ESP32

1. Conecte o ESP32 no computador.  
2. Selecione em **Tools → Board → ESP32 Dev Module**.  
3. Selecione a porta:  
   `Tools → Port → COMX`

Clique em **Upload**.

### ⚠ Possível erro comum
**“Failed to connect to ESP32: Timeout waiting for packet header”**

➡ Solução: **Segure o botão BOOT** por 1–2 segundos quando o upload começar.

---

## 🔎 8. Lendo os Dados via Serial

Abra o monitor serial:

`Tools → Serial Monitor`

Selecione **115200 baud**.

Exemplo de saída:

GPS: -5.04143, -42.47396, 0.7 m/s
ACC: 0.10, 9.82, 0.40
GYRO: 0.02, -0.01, 0.03
Luminosidade: 264
LoRa: pacote enviado
