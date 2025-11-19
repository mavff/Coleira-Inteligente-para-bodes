import serial
import matplotlib.pyplot as plt
import matplotlib.cm as cm # Para o colormap da seta
from collections import deque
import time
import numpy as np # Para cálculos vetoriais

# --- Configurações ---
PORTA_SERIAL = 'COM4'  # MUDE ISSO!
BAUD_RATE = 115200
TAMANHO_HISTORICO_LUZ = 100
# ---------------------

# --- Configurações dos Gráficos ---
LIMITE_ACELEROMETRO_XY = 12 # Limite dos eixos X/Y do acelerômetro para a seta
LIMITE_ACELEROMETRO_Z_COR = 15 # Limite para mapear a aceleração Z para cor (Ex: -15 a +15 m/s^2)
CMAP_Z = 'coolwarm' # Colormap para o eixo Z (azul para negativo, vermelho para positivo)

# --- Conexão Serial ---
try:
    ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial {PORTA_SERIAL}: {e}")
    exit()

print(f"Conectado a {PORTA_SERIAL}. Iniciando dashboard com setas...")
time.sleep(2)

# --- Configuração do Dashboard ---
plt.ion()
fig = plt.figure(figsize=(15, 7))
fig.suptitle("Dashboard de Sensores ESP32", fontsize=16)

# --- Gráfico 1: Acelerômetro 2D com Seta (na esquerda) ---
ax1 = fig.add_subplot(1, 2, 1) # Agora é um subplot 2D
ax1.set_title("Direção de Inclinação (X/Y) e Aceleração Z (Cor)")
ax1.set_xlim([-LIMITE_ACELEROMETRO_XY, LIMITE_ACELEROMETRO_XY])
ax1.set_ylim([-LIMITE_ACELEROMETRO_XY, LIMITE_ACELEROMETRO_XY])
ax1.set_aspect('equal', adjustable='box') # Garante que X e Y tenham a mesma escala
ax1.grid(True)
ax1.set_xlabel("Eixo X (m/s^2)")
ax1.set_ylabel("Eixo Y (m/s^2)")

# Vamos criar uma seta (quiver) no centro (0,0)
# U=0, V=0 são os componentes da seta. Color=None por enquanto.
# O 'quiver' retorna uma coleção de setas.
quiver_plot = ax1.quiver(0, 0, 0, 0, color='blue', scale=1, angles='xy', scale_units='xy')

# Adiciona um círculo no centro para referência
ax1.add_patch(plt.Circle((0, 0), 0.5, color='gray', alpha=0.5, fill=True))


# --- Gráfico 2: Sensor de Luz 2D (na direita) ---
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_title("Histórico de Luminosidade (Lux)")
ax2.set_xlabel("Tempo (amostras)")
ax2.set_ylabel("Luminosidade (Lux)")
ax2.set_ylim(0, 1500) # Começa com um limite fixo, mas vai auto-ajustar
ax2.set_xlim(0, TAMANHO_HISTORICO_LUZ)
ax2.grid(True)

dados_lux = deque([0] * TAMANHO_HISTORICO_LUZ, maxlen=TAMANHO_HISTORICO_LUZ)
eixo_x_lux = list(range(TAMANHO_HISTORICO_LUZ))
linha_lux, = ax2.plot(eixo_x_lux, list(dados_lux), 'b-')

# Colormap para o eixo Z
cmap_z_norm = cm.ScalarMappable(cmap=CMAP_Z)
cmap_z_norm.set_array([-LIMITE_ACELEROMETRO_Z_COR, LIMITE_ACELEROMETRO_Z_COR]) # Define a escala de cores
fig.colorbar(cmap_z_norm, ax=ax1, label="Aceleração Z (m/s^2)") # Adiciona a barra de cores

# Limpa o buffer serial
ser.readline()

try:
    while True:
        data_line = ser.readline().decode('utf-8').strip()

        if data_line:
            try:
                x_str, y_str, z_str, lux_str = data_line.split(',')
                x_val = float(x_str)
                y_val = float(y_str)
                z_val = float(z_str)
                lux_val = float(lux_str)

                # --- 2. Atualizar Gráfico 1 (Seta) ---
                # Aceleração XY (magnitude) para o comprimento da seta
                magnitude_xy = np.sqrt(x_val**2 + y_val**2)

                # Normaliza o valor Z para a escala de cores
                norm_z_val = (z_val + LIMITE_ACELEROMETRO_Z_COR) / (2 * LIMITE_ACELEROMETRO_Z_COR)
                norm_z_val = np.clip(norm_z_val, 0, 1) # Garante que esteja entre 0 e 1
                cor_seta = cmap_z_norm.to_rgba(z_val) # Pega a cor baseada no valor Z

                # Remove a seta antiga e desenha uma nova para atualizar a cor
                quiver_plot.remove()
                quiver_plot = ax1.quiver(0, 0, x_val, y_val, color=cor_seta, scale=1, angles='xy', scale_units='xy', width=0.03)

                # --- 3. Atualizar Gráfico 2 (Luz) ---
                dados_lux.append(lux_val)
                linha_lux.set_ydata(list(dados_lux))
                ax2.relim()
                ax2.autoscale_view(True, True, True)

                # --- 4. Redesenhar ---
                plt.pause(0.01)

            except (ValueError, IndexError):
                print(f"Ignorando linha mal formatada: {data_line}")
            except Exception as e:
                print(f"Erro inesperado: {e}")

except KeyboardInterrupt:
    print("Parando dashboard...")

finally:
    ser.close()
    plt.ioff()
    plt.show()
    print("Conexão serial fechada.")