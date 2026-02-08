import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Força de Trabalho em TI no Brasil | Machine Learning", 
    page_icon="💻", 
    layout="wide"
)

# No título principal do dashboard
st.title("💻 Força de Trabalho em TI no Brasil: Uma Abordagem de Machine Learning")

# Estilização customizada
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 32px; color: #00d4ff; }
    .highlight { background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- DICIONÁRIOS DE TRADUÇÃO (Baseado no seu script e artigo) ---
mapa_uf_nome = {11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO', 21: 'MA', 22: 'PI', 23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA', 31: 'MG', 32: 'ES', 33: 'RJ', 35: 'SP', 41: 'PR', 42: 'SC', 43: 'RS', 50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF'}
mapa_regiao = {'RO':'Norte','AC':'Norte','AM':'Norte','RR':'Norte','PA':'Norte','AP':'Norte','TO':'Norte','MA':'Nordeste','PI':'Nordeste','CE':'Nordeste','RN':'Nordeste','PB':'Nordeste','PE':'Nordeste','AL':'Nordeste','SE':'Nordeste','BA':'Nordeste','MG':'Sudeste','ES':'Sudeste','RJ':'Sudeste','SP':'Sudeste','PR':'Sul','SC':'Sul','RS':'Sul','MS':'Centro-Oeste','MT':'Centro-Oeste','GO':'Centro-Oeste','DF':'Centro-Oeste'}
mapa_edu = {1: 'Sem instrução', 2: 'Fund. Incompleto', 3: 'Fund. Completo', 4: 'Médio Incompleto', 5: 'Médio Completo', 6: 'Sup. Incompleto', 7: 'Sup. Completo'}

@st.cache_data
def load_data():
    # Carregamento inicial
    df = pd.read_csv('dados/profissionais_tic_encontrados.csv')
    
    # --- FILTRO DE QUALIFICAÇÃO ---
    # Mantemos apenas profissionais com Ensino Médio Completo ou superior (códigos >= 5)
    # Isso alinha o dashboard com o foco do artigo em técnicos e graduados
    df = df[df['Nível_Educação'] >= 5]
    
    # Mapeamentos e Traduções
    df['Sigla_UF'] = df['Estado'].map(mapa_uf_nome)
    df['Regiao'] = df['Sigla_UF'].map(mapa_regiao)
    df['Gênero'] = df['Gênero'].map({1: 'Masculino', 2: 'Feminino'})
    df['Escolaridade'] = df['Nível_Educação'].map(mapa_edu)
    
    # Tratamento da Faixa Etária
    faixas_idade = [14, 24, 34, 44, 54, 110]
    rotulos_idade = ['14-24', '25-34', '35-44', '45-54', '55+']
    df['Faixa_Etaria'] = pd.cut(df['Idade'], bins=faixas_idade, labels=rotulos_idade, right=False)
    
    # Classificação dos Perfis Profissionais
    # Dividimos a análise entre Graduados e Técnicos conforme a metodologia do estudo 
    cod_sup = [1330, 2151, 2153, 2166, 2356, 2434, 2511, 2512, 2513, 2514, 2519, 2521, 2522, 2523, 2529]
    df['Perfil'] = df['Código_Ocupação_TI'].apply(
        lambda x: 'Graduados (Nível Superior)' if x in cod_sup else 'Técnicos (Nível Médio)'
    )
    
    return df

df = load_data()

# --- BARRA LATERAL (Filtros Analíticos) ---
st.sidebar.header("🔍 Filtros de Análise")
st.sidebar.write("Ajuste os filtros para atualizar as médias e gráficos em tempo real.")
regioes = st.sidebar.multiselect("Região:", df['Regiao'].unique(), default=df['Regiao'].unique())
genero = st.sidebar.radio("Gênero:", ["Todos", "Masculino", "Feminino"])

df_f = df[df['Regiao'].isin(regioes)]
if genero != "Todos": df_f = df_f[df_f['Gênero'] == genero]

# --- MÉTRICAS E MÉDIA SALARIAL ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Média Salarial (Amostra)", f"R$ {df_f['Renda_Mensal'].mean():.2f}")
c2.metric("Mediana Salarial", f"R$ {df_f['Renda_Mensal'].median():.2f}")
c3.metric("Acurácia (Sup.)", "64,4%")
c4.metric("Acurácia (Téc.)", "69,0%")

st.divider()


# Adicione "Introdução" na criação das abas
tab0, tab1, tab2, tab3 = st.tabs(["📄 Sobre o Projeto", "🌍 Visão Geográfica", "🎓 Nível Superior", "🛠️ Nível Técnico"])

with tab0:
    st.header("📄 Sobre a Pesquisa")
    
    col_intro, col_img = st.columns([2, 1])
    
    with col_intro:
        st.markdown("""
        ### Objetivo
        Este dashboard apresenta os resultados da pesquisa sobre a **Força de Trabalho em Tecnologia no Brasil**, 
        focada em identificar os preditores de renda para profissionais de níveis Médio/Técnico e Superior.
        
        A análise utiliza técnicas de **Machine Learning (XGBoost)** para entender quais características 
        (como idade, localização e tipo de vínculo) exercem maior influência na remuneração do setor.
        """)
        
        st.markdown("""
        ### Fonte de Dados
        Os dados foram extraídos da **PNAD Contínua 2023 (IBGE)**, especificamente filtrando ocupações da 
        classificação de Tecnologia da Informação e Comunicação (TIC). 
        
        **Recorte da Amostra:**
        * Profissionais ativos no setor de tecnologia.
        * Escolaridade a partir do Ensino Médio Completo.
        * Filtragem de outliers para garantir a fidelidade das médias salariais.
        """)
    
    with col_img:
        # Cria três sub-colunas: a do meio recebe a imagem
        c_spacer1, c_logo, c_spacer2 = st.columns([1, 2, 1])
        
        with c_logo:
            st.image("./assets/if.png", width=400) 
            
        st.info(f"""
        **Apresentado em:** 2º SIMCADS - IFSP Cubatão
        **Autora:** Laysa Bernardes
        **Modelo:** XGBoost (Acurácia até 69%)
        """)

    st.divider()

    # Seção de Metodologia Curta
    st.subheader("🔬 Metodologia de Análise")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.write("**1. Coleta e Limpeza**")
        st.caption("Processamento de microdados brutos do IBGE para isolar o setor de tecnologia.")
    
    with m2:
        st.write("**2. Modelagem IA**")
        st.caption("Aplicação de algoritmos de Gradiente Boosting para identificar padrões de renda.")
    
    with m3:
        st.write("**3. Interpretação**")
        st.caption("Tradução dos pesos estatísticos em insights práticos para o mercado de trabalho.")

    st.success("⬅️ Navegue pelas abas acima para explorar as análises detalhadas por perfil profissional.")

with tab1:
    st.subheader("🌎 Panorama Geográfico e Econômico do Setor")
    
    st.markdown("""
    A distribuição da força de trabalho tecnológica no Brasil é um reflexo direto da infraestrutura econômica do país. 
    Esta seção analisa a centralização de talentos e como a maturidade dos polos regionais dita as regras de remuneração 
    e competitividade no mercado nacional.
    """)

    # --- SEÇÃO 1: PARTICIPAÇÃO DE MERCADO ---
    col1_pie, col1_txt = st.columns([2, 1])
    
    with col1_pie:
        fig_pie = px.pie(
            df_f, names="Regiao", 
            hole=0.4,
            title="Market Share: Concentração de Talentos por Região",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col1_txt:
        st.markdown("### 📊 Densidade Regional")
        st.write("""
            O **Sudeste (39%)** e o **Sul (23,2%)** somam mais de 60% da força de trabalho ativa em tecnologia no Brasil. 
            Essa hiperconcentração cria um ecossistema de alta rotatividade e forte disputa por talentos.
        """)
        st.info("""
            **Análise:** O volume massivo nestas regiões atrai investimentos e sedes de Big Techs, 
            consolidando-as como os principais hubs de inovação e educação do país.
        """)

    st.divider()

    # --- SEÇÃO 2: DISPERSÃO SALARIAL ---
    col2_box, col2_txt = st.columns([2, 1])
    
    with col2_box:
        # Gráfico de Box Plot com escala ajustada para clareza
        fig_box = px.box(
            df_f, x="Regiao", y="Renda_Mensal", color="Regiao", 
            log_y=True, points="outliers", 
            range_y=[200, 60000],
            title="Arquitetura de Renda: Dispersão e Outliers por Região"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col2_txt:
        st.markdown("### 💰 Estrutura da Renda")
        st.write("""
            As caixas alongadas no **Sul e Sudeste** revelam mercados com alta amplitude térmica salarial. 
            Isso significa que, embora a base seja competitiva, o teto é extremamente flexível para especialistas.
        """)
        st.success("""
            **Destaque Técnico:** Regiões como o **Nordeste** (18,2% do mercado) apresentam uma estrutura de renda mais 
            agrupada. Isso sugere uma valorização mais homogênea, com menos desigualdade entre cargos de mesma senioridade.
        """)

    # --- SEÇÃO 3: INSIGHTS MACROECONÔMICOS ---
    # --- SEÇÃO 3: INSIGHTS MACROECONÔMICOS ---
    st.divider()
    st.markdown("### 💡 Conclusões Estratégicas sobre o Mercado")

    inf_c1, inf_c2 = st.columns(2)

    with inf_c1:
        st.markdown("**Estratificação Salarial:**")
        # Valores travados conforme a amostra real do projeto
        st.write("""A média salarial da amostra (5.813,17) é significativamente 
            influenciada pelos outliers das grandes regiões metropolitanas. 
            Para uma análise mais realista, a mediana de 3.500,00 deve ser 
            utilizada como o indicador fiel da posição do profissional no mercado.
        """)

    with inf_c2:
        st.markdown("**Custo de Oportunidade:**")
        st.write("""
            Trabalhar em polos maduros (Sudeste e Sul) oferece os maiores tetos salariais, mas exige alta 
            especialização para romper a média. Em contrapartida, polos emergentes (como o Nordeste) 
            apresentam trajetórias de carreira mais lineares e previsíveis, com maior segurança para perfis técnicos.
        """)

    # Resumo Executivo final
    st.info("💡 **Resumo Executivo:** O mercado de tecnologia brasileiro não é homogêneo; ele é composto por submercados regionais com regras de valorização e barreiras de entrada distintas.")
with tab2:
    st.subheader("🎓 Análise Aprofundada: Nível Superior")
    
    # Garantindo que a variável df_s esteja definida
    df_s = df_f[df_f['Perfil'] == 'Graduados (Nível Superior)']
    
    # --- SEÇÃO 1: IDADE (O PRINCIPAL PREDITOR) ---
    st.markdown("### 🧠 1. O Impacto da Experiência e Faixa Etária")
    st.markdown("""
    Diferente de outros setores, o mercado de elite de TI valoriza a combinação entre a base acadêmica sólida 
    e o auge da produtividade técnica. Profissionais entre **25 e 34 anos** estão no epicentro dessa 
    valorização, representando o perfil de capital humano mais dinâmico e valioso para este segmento.
    """)
    
    ordem_idade = ['14-24', '25-34', '35-44', '45-54', '55+']
    fig_idade = px.histogram(
        df_s, x="Faixa_Etaria", color="Gênero", barmode="group",
        title="Distribuição por Faixa Etária e Gênero",
        category_orders={"Faixa_Etaria": ordem_idade},
        height=450
    )
    st.plotly_chart(fig_idade, use_container_width=True)
    
    st.divider()

    # --- SEÇÃO 2: O CÉREBRO DO MODELO (FEATURE IMPORTANCE) ---
    st.markdown("### 🧬 2. Fatores Determinantes de Renda (IA)")
    
    col_feat_s, col_feat_txt_s = st.columns([1.5, 1])
    
    with col_feat_s:
        # Dados extraídos do seu artigo para o nível superior
        dados_imp_s = {
            'Variável': ['Faixa Etária (25-34)', 'Anos de Estudo', 'Atividade Principal', 'Gênero', 'Região'],
            'Importância': [0.23, 0.15, 0.10, 0.06, 0.05] # 0.23 conforme seu artigo
        }
        df_imp_s = pd.DataFrame(dados_imp_s).sort_values(by='Importância', ascending=True)
        
        fig_imp_s = px.bar(
            df_imp_s, x='Importância', y='Variável', orientation='h',
            title="Ranking de Decisão - Nível Superior (XGBoost)",
            color_discrete_sequence=['#00d4ff']
        )
        st.plotly_chart(fig_imp_s, use_container_width=True)

    with col_feat_txt_s:
        st.markdown("#### Por que a Idade lidera?")
        st.write("""
            Conforme o modelo XGBoost, a **Faixa Etária** é o principal preditor (0.23), seguida pelos **Anos de Estudo**.
        """)
        st.info("""
            **Análise:** Isso indica que, para graduados, o mercado recompensa a agilidade e o conhecimento 
            atualizado. A fase da carreira onde o profissional já é produtivo, mas mantém alta capacidade de 
            adaptação, é a característica mais valiosa.
        """)

    st.divider()

    # --- SEÇÃO 3: ESCOLARIDADE E GÊNERO ---
    st.markdown("### ⚖️ 3. Escolaridade e Desigualdade de Ocupação")
    st.markdown("""
    Embora o diploma seja o 'pré-requisito' de entrada, os dados revelam uma disparidade numérica acentuada 
    entre os gêneros. A baixa representatividade feminina nos dados de nível superior sugere barreiras 
    estruturais que limitam o acesso de mulheres graduadas aos postos de elite do setor.
    """)

    fig_edu = px.histogram(
        df_s, x="Escolaridade", color="Gênero", barmode="group",
        title="Nível de Instrução por Gênero",
        category_orders={"Escolaridade": ["Sup. Completo", "Sup. Incompleto", "Médio Completo"]},
        height=450
    )
    st.plotly_chart(fig_edu, use_container_width=True)

    st.info("💡 **Conclusão Técnica:** O sucesso neste perfil depende de uma base acadêmica sólida aliada à manutenção da relevância técnica durante a janela de maior valorização do mercado.")

with tab3:
    st.subheader("🛠️ Análise Técnica: Vínculo, Geografia e Fatores de Decisão")
    
    # Variável filtrada para o grupo técnico
    df_t = df_f[df_f['Perfil'] == 'Técnicos (Nível Médio)']
    mediana_tecnica = 2800

    st.markdown(f"""
    A análise do perfil técnico revela um mercado de **alicerce operacional**. Diferente do nível superior, 
    onde a idade impulsiona a renda, aqui o sucesso é definido pela **estabilidade do vínculo** e pela 
    **localização em polos regionais específicos**. A maioria dos profissionais neste grupo 
    possui uma renda situada na faixa de **R$ {mediana_tecnica}**.
    """)

    # --- ITEM 1: FORMALIZAÇÃO ---
    st.markdown("### 📝 1. O Impacto da Carteira Assinada")
    df_t['Formalizado'] = df_t['Carteira_Assinada'].map({1: 'Com Carteira', 2: 'Informal/Outros'})

    col1, col1_txt = st.columns([2, 1])
    with col1:
        fig_formal = px.histogram(
            df_t, x="Formalizado", y="Renda_Mensal", color="Gênero", 
            histfunc="avg", barmode="group",
            title="Média Salarial por Tipo de Vínculo (Nível Técnico)"
        )
        st.plotly_chart(fig_formal, use_container_width=True)
    with col1_txt:
        st.markdown("#### Insight de Valorização")
        st.write("""
            Ter **Carteira Assinada** é o fator de maior peso (0.16) para o sucesso deste perfil. 
            A formalização é o que separa a base salarial de remunerações mais competitivas.
        """)

    st.divider()

    # --- ITEM 2: IMPORTÂNCIA DAS VARIÁVEIS (O CÉREBRO DO MODELO) ---
    st.markdown("### 🧠 2. Fatores Determinantes na Visão da Inteligência Artificial")
    
    col_feat, col_feat_txt = st.columns([1.5, 1])
    with col_feat:
        # Dados baseados no seu gráfico de Feature Importance do XGBoost
        dados_imp = {
            'Variável': ['Carteira Assinada', 'Região: Nordeste', 'Atividade Principal', 'Anos de Estudo', 'Horas Trabalhadas'],
            'Importância': [0.16, 0.11, 0.09, 0.08, 0.07]
        }
        df_imp = pd.DataFrame(dados_imp).sort_values(by='Importância', ascending=True)
        fig_imp = px.bar(df_imp, x='Importância', y='Variável', orientation='h', 
                         title="Ranking de Decisão (O que a IA prioriza)", color_discrete_sequence=['#00d4ff'])
        st.plotly_chart(fig_imp, use_container_width=True)

    with col_feat_txt:
        st.markdown("#### Por que o Nordeste se destaca na IA?")
        st.write("""
            O modelo identifica o **Nordeste** como o 2º maior preditor de renda (0.11). 
        """)
        st.info("""
            **O Destaque do Nordeste:** Embora o Sudeste tenha mais registros de vagas e salarios, o **Nordeste** é o segundo 
            maior preditor de renda alta (0.11). Isso indica que a região possui polos tecnológicos onde a 
            valorização do técnico é extremamente previsível e constante
        """)    

    st.divider()

    # --- ITEM 3: COMPARATIVO REGIONAL (SUL/SUDESTE VS NORDESTE) ---
    st.markdown("### 📊 3. Comparativo Regional: Médias e Concentração")
    
    col_reg, col_reg_txt = st.columns([2, 1])
    with col_reg:
        # Gráfico que mostra a força real do Sudeste/Sul e Nordeste
        fig_reg_comp = px.histogram(
            df_t, x="Regiao", y="Renda_Mensal", color="Regiao", histfunc="avg",
            title="Média Salarial Técnica por Região do Brasil",
            category_orders={"Regiao": ["Sudeste", "Sul", "Centro-Oeste", "Nordeste", "Norte"]},
            range_y=[0, 6000]
        )
        st.plotly_chart(fig_reg_comp, use_container_width=True)

    with col_reg_txt:
        st.markdown("#### Análise de Mercado")
        st.write("""
            O **Sudeste e o Sul** continuam liderando em termos de valores absolutos e volume de vagas. 
        """)
        st.success("""
            **Conclusão:** O mercado técnico é binário: busca o **volume** e salários de ponta nos 
            eixos Sul-Sudeste, ou a **estabilidade** e o crescimento estratégico em polos do Nordeste.
        """)

st.markdown("---")
st.markdown("### 👥 Créditos e Autoria")

st.write("""
Este dashboard é um desdobramento técnico da pesquisa intitulada **"Emprego de Modelos de IA Generativa no Ensino Assistido: Uma Nova Abordagem ao Pair Programming"**, 
apresentada originalmente no **2º SIMCADS - IFSP Cubatão**.
""")

col_cred1, col_cred2 = st.columns(2)

with col_cred1:
    st.markdown("**💻 Desenvolvimento do Dashboard**")
    st.write("> **Laysa Bernardes**")
    st.caption("Responsável pela arquitetura de dados, design de interface (UX/UI) e implementação do sistema interativo em Streamlit.")

with col_cred2:
    st.markdown("**🔬 Equipe de Pesquisa (Coautores)**")
    st.write("Laysa Bernardes, Lucas Lopes, Beatriz Bastos, Eduardo Miranda, Maria E. Fodor, Miguel Luizatto e Pedro Xavier.")
    st.caption(f"Trabalho orientado pelo **Prof. Me. Paulo Mannini**.")

st.info("💡 **Nota de Transparência:** Este ambiente interativo foi desenvolvido de forma independente por Laysa Bernardes como um projeto de portfólio para visualização avançada dos resultados obtidos pelo grupo de pesquisa.")