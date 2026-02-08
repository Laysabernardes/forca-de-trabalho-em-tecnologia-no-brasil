import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# --- 1. CARREGAR E PREPARAR OS DADOS ---
try:
    df = pd.read_csv('profissionais_tic_encontrados.csv')
except FileNotFoundError:
    print("ERRO: Arquivo 'profissionais_tic_encontrados.csv' não encontrado.")
    print("Certifique-se de executar o script 'ler_panda.py' primeiro.")
    exit()

# Limpar dados: remover linhas sem informação de renda ou horas trabalhadas
df.dropna(subset=['Renda_Mensal', 'Horas_Trabalhadas_Semana'], inplace=True)
print(f"Base de dados carregada com {len(df)} registros válidos.")

# --- Feature Engineering: Criar a variável 'Regiao' ---
mapa_regiao = {
    'Rondônia': 'Norte', 'Acre': 'Norte', 'Amazonas': 'Norte', 'Roraima': 'Norte', 'Pará': 'Norte', 'Amapá': 'Norte', 'Tocantins': 'Norte',
    'Maranhão': 'Nordeste', 'Piauí': 'Nordeste', 'Ceará': 'Nordeste', 'Rio Grande do Norte': 'Nordeste', 'Paraíba': 'Nordeste', 'Pernambuco': 'Nordeste', 'Alagoas': 'Nordeste', 'Sergipe': 'Nordeste', 'Bahia': 'Nordeste',
    'Minas Gerais': 'Sudeste', 'Espírito Santo': 'Sudeste', 'Rio de Janeiro': 'Sudeste', 'São Paulo': 'Sudeste',
    'Paraná': 'Sul', 'Santa Catarina': 'Sul', 'Rio Grande do Sul': 'Sul',
    'Mato Grosso do Sul': 'Centro-Oeste', 'Mato Grosso': 'Centro-Oeste', 'Goiás': 'Centro-Oeste', 'Distrito Federal': 'Centro-Oeste'
}
# Criamos um mapa de UF
mapa_uf_para_nome = {
    11: 'Rondônia', 12: 'Acre', 13: 'Amazonas', 14: 'Roraima', 15: 'Pará', 16: 'Amapá', 17: 'Tocantins',
    21: 'Maranhão', 22: 'Piauí', 23: 'Ceará', 24: 'Rio Grande do Norte', 25: 'Paraíba', 26: 'Pernambuco',
    27: 'Alagoas', 28: 'Sergipe', 29: 'Bahia', 31: 'Minas Gerais', 32: 'Espírito Santo', 33: 'Rio de Janeiro',
    35: 'São Paulo', 41: 'Paraná', 42: 'Santa Catarina', 43: 'Rio Grande do Sul', 50: 'Mato Grosso do Sul',
    51: 'Mato Grosso', 52: 'Goiás', 53: 'Distrito Federal'
}

df['Nome_Estado'] = df['Estado'].map(mapa_uf_para_nome)
df['Regiao'] = df['Nome_Estado'].map(mapa_regiao)
df['Experiencia_Estimada'] = (df['Idade'] - df['Anos_Estudo'] - 6).clip(lower=0)

faixas_idade = [14, 24, 34, 44, 54, 110]
rotulos_idade = ['14-24', '25-34', '35-44', '45-54', '55+']
df['Faixa_Etaria'] = pd.cut(df['Idade'], bins=faixas_idade, labels=rotulos_idade, right=False)

# --- 2. SEPARAR CARREIRAS (TÉCNICO VS. SUPERIOR) ---
codigos_superior = [1330, 2151, 2153, 2166, 2356, 2434, 2511, 2512, 2513, 2514, 2519, 2521, 2522, 2523, 2529]
codigos_tecnico = [3113, 3114, 3522, 3511, 3512, 3513, 3514, 3521, 7421, 7422, 4131, 4132]

df_superior = df[df['Código_Ocupação_TI'].isin(codigos_superior)]
df_tecnico = df[df['Código_Ocupação_TI'].isin(codigos_tecnico)]

print(f"Dados separados em: {len(df_superior)} profissionais de nível superior e {len(df_tecnico)} de nível técnico/médio.")
print("-" * 60)


# --- 3. FUNÇÃO PARA RODAR OS MODELOS (VERSÃO COM OTIMIZAÇÃO) ---
from sklearn.model_selection import RandomizedSearchCV

def analisar_grupo(df_grupo, nome_grupo):
    if len(df_grupo) < 50:
        print(f"\n>>>> GRUPO '{nome_grupo.upper()}' tem dados insuficientes para análise. <<<<")
        return

    print(f"\n>>>> INICIANDO ANÁLISE DO GRUPO: {nome_grupo.upper()} <<<<")

    # Definir as features (X) e o target (y)
    features = [
        'Gênero', 'Cor_Raça', 'Anos_Estudo', 'Horas_Trabalhadas_Semana',
        'Posição_Ocupacional', 'Atividade_Principal', 'Carteira_Assinada', 'Regiao',
        'Experiencia_Estimada', 'Faixa_Etaria'
    ]
    X = df_grupo[features]
    y_class = (df_grupo['Renda_Mensal'] > df_grupo['Renda_Mensal'].median()).astype(int)

    # Identificar tipos de colunas para o pré-processamento
    colunas_numericas = ['Anos_Estudo', 'Horas_Trabalhadas_Semana', 'Experiencia_Estimada']
    colunas_categoricas = ['Gênero', 'Cor_Raça', 'Posição_Ocupacional', 'Atividade_Principal', 'Carteira_Assinada', 'Regiao', 'Faixa_Etaria']

    # Separar dados de treino e teste ANTES da otimização
    X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=0.2, random_state=42, stratify=y_class)

    # Criar o pipeline de pré-processamento
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), colunas_numericas),
            ('cat', OneHotEncoder(handle_unknown='ignore', drop='first'), colunas_categoricas)
        ],
        remainder='passthrough'
    )

    # Pipeline final com o classificador
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', xgb.XGBClassifier(eval_metric='logloss', random_state=42))
    ])

    print("\n--- Otimizando hiperparâmetros do modelo... (Isso pode levar alguns minutos) ---")
    
    # Parâmetros para testar
    param_dist = {
        'classifier__n_estimators': [100, 200, 300, 500],
        'classifier__learning_rate': [0.01, 0.05, 0.1, 0.2],
        'classifier__max_depth': [3, 5, 7, 9],
        'classifier__subsample': [0.7, 0.8, 0.9, 1.0],
        'classifier__colsample_bytree': [0.7, 0.8, 0.9, 1.0]
    }

    # Configurar a busca aleatória
    random_search = RandomizedSearchCV(
        pipeline,
        param_distributions=param_dist,
        n_iter=50,  # Número de combinações a testar. Aumente para uma busca mais exaustiva.
        scoring='accuracy',
        cv=5,       # 5-fold cross-validation
        n_jobs=1,  # Usar todos os processadores
        random_state=42,
        verbose=1   # Mostra o progresso
    )

    # Executar a busca
    random_search.fit(X_train, y_train)

    print(f"\nMelhor Acurácia encontrada na validação cruzada: {random_search.best_score_:.2%}")
    print("Melhores Hiperparâmetros:")
    print(random_search.best_params_)

    # Avaliar o melhor modelo no conjunto de teste
    print("\n--- Avaliação Final no Conjunto de Teste com o Melhor Modelo ---")
    best_model = random_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    print(f"Resultado Acurácia Final: {accuracy_score(y_test, y_pred):.2%}")
    print("Relatório de Classificação Detalhado:")
    print(classification_report(y_test, y_pred, target_names=['Salário Baixo', 'Salário Alto']))
    print("-" * 60)

    print("\n--- Importância das Features ---")
    # Pega o nome das features após o OneHotEncoding
    feature_names = best_model.named_steps['preprocessor'].get_feature_names_out()
    importances = best_model.named_steps['classifier'].feature_importances_
    
    # Cria um DataFrame para melhor visualização
    df_importances = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    print(df_importances.head(15))


# --- 4. EXECUTAR A ANÁLISE PARA CADA GRUPO ---
analisar_grupo(df_superior, "Nível Superior")
analisar_grupo(df_tecnico, "Nível Técnico")