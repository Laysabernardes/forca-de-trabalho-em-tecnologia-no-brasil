# -*- coding: utf-8 -*-
# SCRIPT PARA GERAR GRÁFICO GERAL DA PESQUISA
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

# Configuração de estilo para um gráfico mais bonito
sns.set_theme(style="whitegrid")
plt.style.use('seaborn-v0_8-talk')


print("--- Iniciando Geração de Gráfico Geral da Pesquisa ---")

# --- 1. CARREGAR E PREPARAR OS DADOS ---
try:
    df = pd.read_csv('profissionais_tic_encontrados_anual.csv')
    print("Arquivo CSV carregado com sucesso.")
except FileNotFoundError:
    print("ERRO: Arquivo 'profissionais_tic_encontrados_anual.csv' não encontrado.")
    print("Por favor, execute primeiro o script 'ler_pandas.py' para gerar este arquivo.")
    exit()

# --- 2. LIMPEZA DOS DADOS ---
# Filtra apenas salários válidos (maiores que zero)
df.dropna(subset=['Renda_Mensal'], inplace=True)
df = df[df['Renda_Mensal'] > 0]
df.dropna(subset=['Código_Ocupação_TI'], inplace=True)
print(f"Total de {len(df)} registros com renda válida para análise.")

# --- 3. CRIAR A VARIÁVEL DE SEGMENTAÇÃO ---
# Define os códigos para separar os grupos
codigos_superior = [1330, 2151, 2153, 2166, 2356, 2434, 2511, 2512, 2513, 2514, 2519, 2521, 2522, 2523, 2529]
# Cria a coluna 'Nivel' para o gráfico
df['Nivel'] = np.where(df['Código_Ocupação_TI'].isin(codigos_superior), 'Nível Superior', 'Nível Técnico')

# --- 4. TRATAMENTO DE OUTLIERS (APENAS PARA VISUALIZAÇÃO) ---
# Salários muito altos podem "espremer" o gráfico, dificultando a visualização da maioria.
# Vamos limitar a visualização ao 98º percentil para focar na distribuição principal.
limite_superior = df['Renda_Mensal'].quantile(0.98)
df_visualizacao = df[df['Renda_Mensal'] <= limite_superior]
print(f"Para melhor visualização, o gráfico exibirá rendas de até R$ {limite_superior:,.2f} (98º percentil).")


# --- 5. GERAÇÃO DO GRÁFICO BOX PLOT ---
print("Gerando o Box Plot comparativo de Renda Mensal...")

plt.figure(figsize=(12, 8))
sns.boxplot(x='Nivel', y='Renda_Mensal', data=df_visualizacao, palette='pastel', hue='Nivel', legend=False)

# Adiciona títulos e labels para clareza
plt.title('Distribuição de Renda Mensal por Nível de Formação em TI', fontsize=18, pad=20)
plt.xlabel('Nível de Formação', fontsize=14)
plt.ylabel('Renda Mensal (R$)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Adiciona uma nota sobre o filtro de outliers no rodapé da imagem
plt.figtext(0.5, 0.01, f'Nota: Exibindo dados até o 98º percentil (R$ {limite_superior:,.2f}) para melhor visualização da distribuição.', 
            ha="center", fontsize=10, style='italic')

# Ajusta o layout para garantir que nada seja cortado
plt.tight_layout(rect=[0, 0.05, 1, 1])

# --- 6. SALVAR O GRÁFICO ---
nome_arquivo_grafico = "grafico_boxplot_renda_por_nivel.png"
try:
    plt.savefig(nome_arquivo_grafico, dpi=300) # dpi=300 para alta qualidade
    plt.close()
    print(f"\n--- SUCESSO ---")
    print(f"Gráfico salvo com sucesso como '{nome_arquivo_grafico}'!")
except Exception as e:
    print(f"\nOcorreu um erro ao salvar o gráfico: {e}")