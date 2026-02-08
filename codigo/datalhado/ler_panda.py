import pandas as pd

# --- 1. CONFIGURAÇÃO ---
arquivos_dados = [
    'PNADC_012024.txt',
    'PNADC_022024.txt',
    'PNADC_032024.txt',
    'PNADC_042024.txt'
]
caminho_input = 'input_PNADC_trimestral.sas' 

# Usando os códigos da "Classificação de Ocupações Domiciliares (COD)" para a coluna V4010
codigos_tic_v4010 = [
    # Dirigentes e Gerentes
    1330,  # Dirigentes de serviços de tecnologia da informação e comunicações

    # Profissionais de Nível Superior
    2151,  # Engenheiros eletrônicos
    2153,  # Engenheiros em telecomunicações
    2166,  # Desenhistas gráficos e de multimídia
    2356,  # Instrutores em tecnologias da informação
    2434,  # Profissionais de vendas de tecnologia da informação e comunicações

    # Profissionais de Tecnologias da Informação e Comunicações (Categoria Principal)
    2511,  # Analistas de sistemas
    2512,  # Desenvolvedores de programas e aplicativos (software)
    2513,  # Desenvolvedores de páginas de internet (web) e multimídia
    2514,  # Programadores de aplicações
    2519,  # Desenvolvedores e analistas de programas e aplicativos (software) e multimídia não classificados anteriormente
    2521,  # Desenhistas e administradores de bases de dados
    2522,  # Administradores de sistemas
    2523,  # Profissionais em rede de computadores
    2529,  # Especialistas em base de dados e em redes de computadores não classificados anteriormente

    # Técnicos e Profissionais de Nível Médio
    3113,  # Eletrotécnicos
    3114,  # Técnicos em eletrônica
    3522,  # Técnicos de engenharia de telecomunicações

    # Técnicos de Nível Médio da Tecnologia da informação e das Comunicações (Categoria Principal)
    3511,  # Técnicos em operações de tecnologia da informação e das comunicações
    3512,  # Técnicos em assistência ao usuário de tecnologia da informação e das comunicações
    3513,  # Técnicos de redes e sistemas de computadores
    3514,  # Técnicos da web
    3521,  # Técnicos em radiodifusão e gravação audivisual
    
    # Trabalhadores Especializados em Eletrônica e Eletricidade
    7421,  # Mecânicos e reparadores em eletrônica
    7422,  # Instaladores e reparadores em tecnologia da informação e comunicações

    # Trabalhadores de Apoio a Operadores
    4131,  # Operadores de máquina de processamento de texto e mecanógrafos
    4132,  # Operadores de entrada de dados
]

# Variáveis que vamos usar na análise final
colunas_necessarias = [
    'UF',      # Unidade da Federação
    'V2007',   # Sexo
    'V2009',   # Idade na data de referência
    'V2010',   # Cor ou raça
    'VD3004',  # Nível de instrução mais elevado alcançado (5 anos ou mais de idade)
    'V4010',   # Ocupação no trabalho principal
    'VD4020',  # Rendimento mensal efetivo de todos os trabalhos para pessoas de 14 anos ou mais de idade (apenas pessoas que recebem em dinheiro, produtos ou mercadorias em qualquer trabalho)
    'VD4031',  # Horas habitualmente trabalhadas por semana em todos os trabalhos
    'V4012',   # Posição na ocupação (Empregado, Conta própria, Empregador, etc.)
    'VD4010',  # Grupamento de atividade do trabalho principal
    'V4029',   # Tinha carteira de trabalho assinada neste trabalho
    'VD3005'   # Anos de estudo
]

# --- 2. LER O SCRIPT DE INPUT PARA EXTRAIR A ESTRUTURA ---
print("Iniciando o processo...")
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
    print(f"ERRO: Arquivo de input não encontrado em '{caminho_input}'.")
    exit()
print(f"Estrutura lida com sucesso! {len(nomes_colunas)} colunas encontradas.")

# --- 3. LER E PROCESSAR TODOS OS ARQUIVOS EM PEDAÇOS (CHUNKS) ---
print("Lendo e filtrando os microdados pela coluna V4010...")
lista_de_chunks_ti = []

for arquivo_dados in arquivos_dados:
    print(f"\n--- Processando o arquivo: {arquivo_dados} ---")
    
    tamanho_do_chunk = 100000
    try:
        leitor_de_chunks = pd.read_fwf(
            arquivo_dados,
            colspecs=posicoes_colunas, names=nomes_colunas,
            header=None, chunksize=tamanho_do_chunk
        )
        
        for i, chunk in enumerate(leitor_de_chunks):
            print(f"Processando pedaço {i+1}...")
            
            # FILTRANDO PELA COLUNA CORRETA (V4010)
            chunk.dropna(subset=['V4010'], inplace=True)
            chunk['V4010'] = chunk['V4010'].astype(int)
            chunk_ti = chunk[chunk['V4010'].isin(codigos_tic_v4010)]
            
            if not chunk_ti.empty:
                lista_de_chunks_ti.append(chunk_ti[colunas_necessarias])
    except FileNotFoundError:
        print(f"AVISO: Arquivo '{arquivo_dados}' não encontrado. Pulando para o próximo.")
        continue

# --- 4. ANÁLISE FINAL E EXIBIÇÃO DOS RESULTADOS ---
print("\nJuntando os dados dos profissionais de TI de todos os trimestres...")

if not lista_de_chunks_ti:
    print("\n--- ANÁLISE CONCLUÍDA ---")
    print("Nenhum profissional de TI encontrado com os códigos COD fornecidos na coluna V4010.")
else:
    # Concatena todos os pedaços filtrados em um único DataFrame
    df_ti_final = pd.concat(lista_de_chunks_ti, ignore_index=True)
    
    print(f"\nTotal de profissionais de TI encontrados na amostra: {len(df_ti_final)}")
    print("\n--- DADOS DOS PROFISSIONAIS DE TI ENCONTRADOS (sem cálculo) ---")

    # Para melhor visualização, vamos traduzir os códigos para texto
    # df_ti_final['UF'] = df_ti_final['UF'].map(mapa_uf)
    # df_ti_final['V2007'] = df_ti_final['V2007'].map(mapa_genero)
    # df_ti_final['VD3004'] = df_ti_final['VD3004'].map(mapa_educacao)
    # df_ti_final['V2010'] = df_ti_final['V2010'].map(mapa_cor_raca)

    # Renomeando as colunas para maior clareza
    df_ti_final.rename(columns={
        'UF': 'Estado',
        'V2007': 'Gênero',
        'V2009': 'Idade',
        'V2010': 'Cor_Raça',
        'VD3004': 'Nível_Educação',
        'V4010': 'Código_Ocupação_TI',
        'VD4020': 'Renda_Mensal',
        'VD4031': 'Horas_Trabalhadas_Semana',
        'V4012': 'Posição_Ocupacional',
        'VD4010': 'Atividade_Principal',
        'V4029': 'Carteira_Assinada',
        'VD3005': 'Anos_Estudo'
    }, inplace=True)

    # Salva o DataFrame final em um arquivo CSV
    nome_arquivo_saida = 'profissionais_tic_encontrados.csv'
    try:
        # Usamos index=False para não salvar o índice do DataFrame no arquivo
        # Usamos encoding='utf-8-sig' para garantir a compatibilidade com acentos no Excel
        df_ti_final.to_csv(nome_arquivo_saida, index=False, encoding='utf-8-sig')
        
        print(f"\n--- SUCESSO ---")
        print(f"Os dados foram salvos com sucesso no arquivo: '{nome_arquivo_saida}'")
    
    except Exception as e:
        print(f"\n--- ERRO ---")
        print(f"Ocorreu um erro ao salvar o arquivo CSV: {e}")
