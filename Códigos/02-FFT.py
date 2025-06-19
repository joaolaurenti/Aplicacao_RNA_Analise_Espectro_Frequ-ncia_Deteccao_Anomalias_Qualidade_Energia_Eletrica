"""
Esté código é feito somente para estudo dos sinais feitos com o '01-Gerador_de_sinais.py'
"""

# Bibliotecas
import numpy as np # Biblioteca para operações numéricas e matrizes
import matplotlib.pyplot as plt # Biblioteca para plotagem de gráficos
import pandas as pd # Biblioteca para manipulação de dados (não usada neste script)
from scipy.fft import fft, fftfreq # Funções para cálculo de FFT e frequências correspondentes
import os # Biblioteca para manipulação de caminhos e arquivos

# Definição do identificador do sinal
identificador_sinal = 5 # Escolha do sinal para análise (pode ser alterado para outro número)
output = "02 - Sinais" # Pasta onde os sinais estão armazenados

# Seleção do arquivo com base no identificador
nome_arquivo = os.path.join(output, f'Sinal_{identificador_sinal}.txt')  # Monta o caminho do arquivo do sinal

# Carrega o sinal a partir do arquivo
data = np.loadtxt(nome_arquivo, skiprows=1) # Carrega os dados ignorando o cabeçalho
tempo = data[:, 0] # Primeira coluna é o tempo
sinal = data[:, 1] # Segunda coluna é o sinal

# Cálculo da FFT
N = len(sinal) # Leitura do sinal
T = tempo[1] - tempo[0] # Intervalo de amostragem entre dois pontos consecutivos
fft_resultado = fft(sinal) # Calcula a FFT do sinal
frequencias = fftfreq(N, T)[:N // 2] # Calcula as frequências e mantém apenas a metade positiva
magnitude = 2.0 / N * np.abs(fft_resultado[:N // 2]) # Calcula a magnitude do espectro de frequência

# Identificação da frequência fundamental
indice_fundamental = np.argmax(magnitude) # Encontra o índice com maior magnitude (fundamental)
frequencia_fundamental = frequencias[indice_fundamental] # Frequência correspondente
magnitude_fundamental = magnitude[indice_fundamental] # Magnitude correspondente

# Exibição dos resultados
print(f"Sinal {identificador_sinal:.0f}")                             # Exibe o identificador do sinal
print(f"Frequência fundamental (Hz): {frequencia_fundamental:.0f}")  # Exibe a frequência fundamental
print(f"Magnitude correspondente (V): {magnitude_fundamental:.0f}")  # Exibe a magnitude da fundamental

# Definição dos harmônicos desejados
harmonicos = [2, 3, 4, 5, 6, 7, 8, 9, 10] # Lista dos harmônicos a serem analisados
frequencias_harmonicas = [frequencia_fundamental * h for h in harmonicos] # Calcula as frequências dos harmônicos

# Função para encontrar o índice da frequência mais próxima
def encontrar_indice_frequencia_desejada(frequencias, frequencia_desejada):
    return np.argmin(np.abs(frequencias - frequencia_desejada))  # Retorna o índice mais próximo da frequência desejada

# Encontrar as magnitudes e frequências dos harmônicos
harmonicos_magnitudes = [] # Lista para armazenar as magnitudes dos harmônicos
harmonicos_frequencias = [] # Lista para armazenar as frequências dos harmônicos

for frequencia_harmonica in frequencias_harmonicas: # Para cada frequência harmônica desejada
    indice_harmonico = encontrar_indice_frequencia_desejada(frequencias, frequencia_harmonica)  # Encontra o índice mais próximo
    harmonicos_magnitudes.append(magnitude[indice_harmonico]) # Armazena a magnitude correspondente
    harmonicos_frequencias.append(frequencias[indice_harmonico]) # Armazena a frequência correspondente

# Exibição dos resultados das frequências e magnitudes dos harmônicos
for h, f_h, mag_h in zip(harmonicos, harmonicos_frequencias, harmonicos_magnitudes):
    print(f"Harmônico {h}: Frequência = {f_h:.0f} Hz, Magnitude = {mag_h:.3f} V")  # Exibe cada harmônico

# cálculo da THD (Distorção Harmônica Total)
thd = np.sqrt(np.sum(np.square(harmonicos_magnitudes))) / magnitude_fundamental # Calcula a THD
print(f"THD: {thd:.2%}") # Exibe a THD em porcentagem

# Avaliação qualitativa da THD
if thd > 0.10:
    print("Crítico") 
elif 0.08 < thd <= 0.10:
    print("Precário") 
elif thd <= 0.08:
    print("Adequado") 

# Extração de um período do sinal
periodo_sinal = 1 / frequencia_fundamental                              # Calcula a duração de um período
indice_periodo = np.where(tempo >= periodo_sinal)[0][0]                 # Encontra o índice que representa um período completo
tempo_periodo = tempo[:indice_periodo]                                  # Recorta o tempo correspondente a um período
sinal_periodo = sinal[:indice_periodo]                                  # Recorta o sinal correspondente a um período

indices_selecionados = np.linspace(0, len(tempo_periodo) -1, num=100, dtype=int)  # Seleciona 100 pontos uniformemente no período



# Plotagem dos gráficos---------------------------------------------------------------------------------------------------------------------

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 6))  # Cria uma figura com 3 subplots verticais
'''
# Gráfico do sinal no domínio do tempo
ax1.set_title(f'Sinal {identificador_sinal} no Domínio do Tempo')  # Título do gráfico
ax1.set_xlabel('Tempo [s]')                                        # Rótulo do eixo X
ax1.set_ylabel('Amplitude [V]')                                    # Rótulo do eixo Y
ax1.plot(tempo, sinal)                                             # Plota o sinal
ax1.grid()                                                         # Adiciona grade
'''

# Gráfico do sinal no domínio do tempo
ax1.set_title(f'Sinal Crítico')  # Título do gráfico
ax1.set_xlabel('Tempo [s]')                                        # Rótulo do eixo X
ax1.set_ylabel('Amplitude [V]')                                    # Rótulo do eixo Y
ax1.plot(tempo, sinal)                                             # Plota o sinal
ax1.grid()   

# Gráfico do espectro de frequência (FFT)
ax2.set_title('FFT')                                               # Título do gráfico
ax2.set_xlabel('Frequência [Hz]')                                  # Rótulo do eixo X
ax2.set_ylabel('Magnitude [V]')                                    # Rótulo do eixo Y
ax2.plot(frequencias, magnitude)                                   # Plota o espectro de frequência
ax2.grid()                                                         # Adiciona grade

# gráfico de um período 
#ax3.set_title(f'Período Discretizado - Sinal {identificador_sinal}') # Título do gráfico
ax3.set_title(f'Período Discretizado - Sinal {identificador_sinal}')             # Título do gráfico
ax3.set_xlabel('Tempo [s]')                                        # Rótulo do eixo X
ax3.set_ylabel('Magnitude [V]')                                    # Rótulo do eixo Y
ax3.scatter(tempo_periodo[indices_selecionados], sinal_periodo[indices_selecionados])  # Plota pontos do sinal em um período
ax3.grid()                                                         # Adiciona grade

plt.tight_layout()                                                 # Ajusta layout para evitar sobreposição
plt.show()

# Plotagem lado a lado
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))  # Uma linha, dois gráficos

# gráfico de um período 
ax1.set_title(f'Período Discretizado - Sinal Crítico')             
ax1.set_xlabel('Tempo [s]')                                        
ax1.set_ylabel('Magnitude [V]')                                    
ax1.scatter(tempo_periodo[indices_selecionados], sinal_periodo[indices_selecionados])  
ax1.grid()                                                         

# Gráfico da FFT
ax2.plot(frequencias, magnitude)
ax2.set_title("Espectro de Frequência (FFT)")
ax2.set_xlabel("Frequência [Hz]")
ax2.set_ylabel("Magnitude [V]")
ax2.grid(True)

plt.tight_layout()
plt.show()                                                         


