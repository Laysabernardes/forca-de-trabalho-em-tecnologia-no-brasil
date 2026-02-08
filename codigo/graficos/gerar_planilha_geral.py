import pandas as pd
import os

# --- 1. CONFIGURAÇÃO ---
arquivos_dados = [
    'PNADC_2023_trimestre4.txt' 
]
caminho_input = 'input_PNADC_trimestre4_20240425.txt' 

# O NOME DO ARQUIVO CSV DE SAÍDA FOI ALTERADO PARA REFLETIR O NOVO CONTEÚDO
nome_arquivo_saida = 'forca_de_trabalho_geral_2023.csv'

# A LISTA DE CÓDIGOS DE TI NÃO É MAIS USADA, MAS MANTEMOS PARA REFERÊNCIA
# codigos_tic_v4010 = [...] 

# Variáveis que vamos usar na análise final (as mesmas de antes)
colunas_necessarias = [
    'UF', 'V2007', 'V2009', 'V2010', 'VD3004', 'V4010', 'VD4020',
    'VD4031', 'V4012', 'VD4010', 'V4029', 'VD3005'
]

# --- 2. LER O DICIONÁRIO ---
print("--- Iniciando Leitura dos Microdados para TODA A FORÇA DE TRABALHO ---")
print(f"Lendo estrutura do dicionário: '{caminho_input}'")
nomes_colunas = []
posicoes_colunas = []
try:
    with open(caminho_input, 'r', encoding='latin-1') as f:
        for linha in f:
            linha = linha.strip()
            if linha.startswith('@'):
                partes = linha.split()
                pos_inicial = int(partes[0].replace('@', ''))
                nome_variavel = partes[1]
                tamanho_str = partes[2].replace('.', '').replace('$', '')
                tamanho = int(tamanho_str)
                pos_final = pos_inicial + tamanho
                nomes_colunas.append(nome_variavel)
                posicoes_colunas.append((pos_inicial - 1, pos_final - 1))
except FileNotFoundError:
    print(f"ERRO: Arquivo de input '{caminho_input}' não encontrado.")
    exit()
print(f"Estrutura lida com sucesso! {len(nomes_colunas)} colunas encontradas.")

# --- 3. LER, FILTRAR (APENAS OCUPADOS) E SALVAR DIRETAMENTE NO CSV ---
print(f"Processando dados para salvar em '{nome_arquivo_saida}'...")

if os.path.exists(nome_arquivo_saida):
    os.remove(nome_arquivo_saida)

header_escrito = False
total_registros_salvos = 0

for arquivo_dados_atual in arquivos_dados:
    print(f"\n--- Processando o arquivo: {arquivo_dados_atual} ---")
    tamanho_do_chunk = 50000
    
    try:
        leitor_de_chunks = pd.read_fwf(
            arquivo_dados_atual,
            colspecs=posicoes_colunas, names=nomes_colunas,
            header=None, chunksize=tamanho_do_chunk
        )
        
        for i, chunk in enumerate(leitor_de_chunks):
            print(f"Processando pedaço {i+1}...")
            
            # MUDANÇA PRINCIPAL AQUI!
            # 1. Mantemos apenas as pessoas que têm um código de ocupação (não são nulos)
            chunk.dropna(subset=['V4010'], inplace=True)
            
            # 2. A LINHA QUE FILTRAVA POR CÓDIGOS DE TI FOI REMOVIDA.
            # chunk_ti = chunk[chunk['V4010'].isin(codigos_tic_v4010)] # <= LINHA REMOVIDA
            
            # Agora, 'chunk' contém todos os trabalhadores, não apenas os de TI.
            if not chunk.empty:
                chunk_final = chunk[colunas_necessarias].copy()
                
                chunk_final.rename(columns={
                    'UF': 'Estado', 'V2007': 'Gênero', 'V2009': 'Idade', 'V2010': 'Cor_Raça',
                    'VD3004': 'Nível_Educação', 'V4010': 'Código_Ocupação', 'VD4020': 'Renda_Mensal',
                    'VD4031': 'Horas_Trabalhadas_Semana', 'V4012': 'Posição_Ocupacional',
                    'VD4010': 'Atividade_Principal', 'V4029': 'Carteira_Assinada', 'VD3005': 'Anos_Estudo'
                }, inplace=True)
                
                chunk_final.to_csv(
                    nome_arquivo_saida, mode='a', header=not header_escrito, 
                    index=False, encoding='utf-8-sig'
                )
                header_escrito = True
                total_registros_salvos += len(chunk_final)
                print(f"  > {len(chunk_final)} trabalhadores encontrados e salvos no CSV. Total até agora: {total_registros_salvos}")

    except FileNotFoundError:
        print(f"AVISO: Arquivo de dados '{arquivo_dados_atual}' não encontrado.")
        continue

print(f"\n--- SUCESSO ---")
print(f"Os dados da força de trabalho geral foram salvos com sucesso no arquivo: '{nome_arquivo_saida}'")
print(f"Total de registros na planilha final: {total_registros_salvos}")