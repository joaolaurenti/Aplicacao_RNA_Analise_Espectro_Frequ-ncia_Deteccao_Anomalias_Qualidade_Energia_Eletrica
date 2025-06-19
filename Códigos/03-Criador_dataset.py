# Importação das bibliotecas necessárias
import numpy as np                      # Para manipulação de arrays e operações numéricas
import pandas as pd                    # Para criação e manipulação do DataFrame (CSV)
import os                              # Para manipulação de caminhos e verificação de arquivos
from scipy.fft import fft, fftfreq     # Para realizar a Transformada Rápida de Fourier (FFT)

# Caminho da pasta onde estão os arquivos de sinais
pasta_sinais = "02 - Sinais"
quantidade_pontos = 24  # Quantidade de pontos a serem extraídos de um período do sinal

# Inicialização da estrutura do CSV
dados_csv = []
cabecalho = ["Sinais"]  # Primeira coluna: identificador do sinal
for i in range(1, quantidade_pontos + 1):
    cabecalho.append(f"X_{i}")  # Tempo de cada ponto
    cabecalho.append(f"Y_{i}")  # Amplitude de cada ponto
cabecalho.extend(["THD", "THD_Classificacao"])  # Total Harmonic Distortion e sua classificação
dados_csv.append(cabecalho)  # Adiciona o cabeçalho à estrutura de dados

# Laço para processar cada arquivo de sinal
for identificador in range(1, 1001):
    nome_arquivo = os.path.join(pasta_sinais, f"Sinal_{identificador}.txt")
    if not os.path.isfile(nome_arquivo):  # Verifica se o arquivo existe
        continue

    data = np.loadtxt(nome_arquivo, skiprows=1)  # Carrega os dados ignorando o cabeçalho
    tempo = data[:, 0]  # Coluna de tempo
    sinal = data[:, 1]  # Coluna de sinal

    # Cálculo da FFT
    N = len(sinal)                    # Número de amostras
    T = tempo[1] - tempo[0]           # Intervalo de tempo entre amostras
    fft_resultado = fft(sinal)       # Aplica FFT ao sinal
    frequencias = fftfreq(N, T)[:N // 2]           # Frequências positivas
    magnitude = 2.0 / N * np.abs(fft_resultado[:N // 2])  # Magnitude da FFT normalizada

    # Determina frequência fundamental (maior pico de magnitude)
    indice_fundamental = np.argmax(magnitude)
    freq_fundamental = frequencias[indice_fundamental]
    mag_fundamental = magnitude[indice_fundamental]

    # Seleção dos harmônicos e cálculo da magnitude
    harmonicos = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    harmonicos_magnitudes = []
    for h in harmonicos:
        freq_h = freq_fundamental * h
        idx = np.argmin(np.abs(frequencias - freq_h))  # Índice mais próximo da frequência harmônica
        harmonicos_magnitudes.append(magnitude[idx])

    # Cálculo do THD (Total Harmonic Distortion)
    thd = np.sqrt(np.sum(np.square(harmonicos_magnitudes))) / mag_fundamental

    # Classificação da qualidade com base no THD
    if thd > 0.1:
        classificacao = "Crítico"
    elif 0.08 < thd and thd <= 0.1:
        classificacao = "Precário"
    else:
        classificacao = "Adequado"

    # Determina o período do sinal
    periodo = 1 / freq_fundamental
    try:
        indice_periodo = np.where(tempo >= periodo)[0][0]  # Primeiro índice após um período completo
    except IndexError:
        print(f"Sinal_{identificador} ignorado (sem período completo)")
        continue

    # Extrai o sinal correspondente a um período
    tempo_periodo = tempo[:indice_periodo]
    sinal_periodo = sinal[:indice_periodo]

    # Garante que há pontos suficientes para amostragem
    if len(tempo_periodo) < quantidade_pontos:
        print(f"Sinal_{identificador} ignorado (poucos pontos para amostrar)")
        continue

    # Seleciona uniformemente os pontos desejados
    indices = np.linspace(0, len(tempo_periodo) - 1, quantidade_pontos, dtype=int)
    pontos_x = tempo_periodo[indices]
    pontos_y = sinal_periodo[indices]

    # Monta a linha de dados
    linha = [f"Sinal_{identificador}"]
    for x, y in zip(pontos_x, pontos_y):
        linha.append(x)
        linha.append(y)

    linha.append(thd)
    linha.append(classificacao)

    # Verifica se a linha tem o número certo de colunas
    if len(linha) != len(cabecalho):
        print(f"Sinal_{identificador} ignorado (coluna incompleta)")
        continue

    dados_csv.append(linha)  # Adiciona a linha aos dados

# Salva os dados em um arquivo CSV
if dados_csv[1:]:  # Verifica se há linhas válidas (exclui cabeçalho)
    df_resultado = pd.DataFrame(dados_csv[1:], columns=dados_csv[0])
    df_resultado.to_csv("DataSet.csv", index=False)
    print("CSV gerado com sucesso")
else:
    print("Nenhum sinal válido encontrado para gerar o CSV")
