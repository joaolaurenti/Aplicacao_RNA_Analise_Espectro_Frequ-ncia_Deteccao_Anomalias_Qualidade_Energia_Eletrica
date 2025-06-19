import matplotlib.pyplot as plt  # Biblioteca para plotar gráficos (não é usada nesse script, mas pode ser útil)
import random                    # Biblioteca para geração de números aleatórios
import numpy as np              # Biblioteca para operações numéricas e manipulação de arrays
import os                       # Biblioteca para operações com o sistema de arquivos (como caminhos de diretórios)

# Parâmetros gerais
amp_fund = 380 # Amplitude fixa da componente fundamental
taxa_amostragem = 1400 # Hz - taxa de amostragem definida com base no teorema da amostragem
freq_fund = 60 # Hz - frequência fundamental, usada como exemplo do sistema brasileiro
duracao = 5 / freq_fund # Duração do sinal em segundos (número de ciclos/frequência)
harmonicos = [2, 3, 4, 5, 6, 7, 8, 9, 10] # Lista de harmônicos a serem adicionados ao sinal

output = "02 - Sinais" # Pasta onde os arquivos dos sinais serão salvos

# Função para gerar 
def gerar_sinal(identificador_sinal):
    # Cria o vetor de tempo com base na duração e taxa de amostragem
    tempo = np.linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False) # Vetor de tempo
    sinal = amp_fund * np.sin(2 * np.pi * freq_fund * tempo) # Geração do sinal senoidal fundamental (60 Hz)

    # Adicionando harmônicos
    sinal_harmonico = sinal.copy()  # Copia o sinal fundamental para adicionar os harmônicos
    for harmonico in harmonicos: # Loop pela lista de harmônicos definidos
        amp_harmonico = amp_fund * (random.uniform(0.001, 0.05))  # Gera uma amplitude aleatória 
        # Adiciona o harmônico ao sinal
        sinal_harmonico += amp_harmonico * np.sin(2 * np.pi * freq_fund * harmonico * tempo)
    
    # Salvando o sinal
    data = np.column_stack((tempo, sinal_harmonico))  # Junta tempo e sinal em colunas
    nome_arquivo = os.path.join(output, f'Sinal_{identificador_sinal}.txt')  # Caminho do arquivo
    np.savetxt(nome_arquivo, data, header='tempo sinal', comments='', fmt=['%.6f', '%.6f'])  # Salva o arquivo com cabeçalho
    print(f"Sinal {identificador_sinal} salvo como {nome_arquivo}")  # Confirmação no terminal

# extrutura de repetição para novos sinais
for identificador_sinal in range(1, 1001):  # Loop para gerar sinais diferentes
    gerar_sinal(identificador_sinal)  # Chama a função de geração para cada sinal
