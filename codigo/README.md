link para a base: https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Trimestre/Trimestre_4/Dados/

Análise com as seguintes features:
```python
features = [
  'Gênero', 'Cor_Raça', 'Anos_Estudo', 'Horas_Trabalhadas_Semana',
  'Posição_Ocupacional', 'Atividade_Principal', 'Carteira_Assinada', 'Regiao',
  'Experiencia_Estimada', 'Faixa_Etaria'
]
```
Resultado:
```bash
--- Iniciando Etapa 2: Modelagem de Machine Learning ---
Base de dados carregada com 4336 registros válidos para modelagem.
Dados separados em: 1788 profissionais de nível superior e 2548 de nível técnico/médio.
------------------------------------------------------------

>>>> INICIANDO ANÁLISE DO GRUPO: NÍVEL SUPERIOR <<<<

--- Otimizando hiperparâmetros do modelo... ---
Fitting 5 folds for each of 50 candidates, totalling 250 fits

Melhor Acurácia encontrada na validação cruzada: 71.61%
Melhores Hiperparâmetros: {'classifier__subsample': 1.0, 'classifier__n_estimators': 300, 'classifier__max_depth': 3, 'classifier__learning_rate': 0.05, 'classifier__colsample_bytree': 0.9}

--- Avaliação Final no Conjunto de Teste com o Melhor Modelo ---
Resultado Acurácia Final: 68.72%
Relatório de Classificação Detalhado:
               precision    recall  f1-score   support

Salário Baixo       0.75      0.64      0.69       193
 Salário Alto       0.64      0.75      0.69       165

     accuracy                           0.69       358
    macro avg       0.69      0.69      0.69       358
 weighted avg       0.70      0.69      0.69       358

------------------------------------------------------------

>>>> INICIANDO ANÁLISE DO GRUPO: NÍVEL TÉCNICO <<<<

--- Otimizando hiperparâmetros do modelo... ---
Fitting 5 folds for each of 50 candidates, totalling 250 fits

Melhor Acurácia encontrada na validação cruzada: 73.60%
Melhores Hiperparâmetros: {'classifier__subsample': 1.0, 'classifier__n_estimators': 500, 'classifier__max_depth': 5, 'classifier__learning_rate': 0.01, 'classifier__colsample_bytree': 0.7}

--- Avaliação Final no Conjunto de Teste com o Melhor Modelo ---
Resultado Acurácia Final: 72.55%
Relatório de Classificação Detalhado:
               precision    recall  f1-score   support

Salário Baixo       0.73      0.73      0.73       257
 Salário Alto       0.73      0.72      0.72       253

     accuracy                           0.73       510
    macro avg       0.73      0.73      0.73       510
 weighted avg       0.73      0.73      0.73       510

--- ANÁLISE COMPLETA CONCLUÍDA ---
```



## RESULTADO TEXTE3 - 22/06/2025
```bash

--- Iniciando Etapa 2: Modelagem de Machine Learning (com Seleção de Features) ---
Base de dados carregada com 3037 registros válidos para modelagem.
Dados separados em: 1248 profissionais de nível superior e 1789 de nível técnico/médio.
------------------------------------------------------------

>>>> INICIANDO ANÁLISE DO GRUPO: NÍVEL SUPERIOR <<<<

--- Otimizando hiperparâmetros do modelo (versão original/simples)... ---
Fitting 5 folds for each of 50 candidates, totalling 250 fits

Melhor Acurácia encontrada na validação cruzada: 67.03%
Melhores Hiperparâmetros: {'classifier__subsample': 1.0, 'classifier__n_estimators': 300, 'classifier__max_depth': 3, 'classifier__learning_rate': 0.01, 'classifier__colsample_bytree': 0.8}

--- Avaliação Final no Conjunto de Teste com o Melhor Modelo ---
Resultado Acurácia Final: 64.40%
Relatório de Classificação Detalhado:
               precision    recall  f1-score   support

Salário Baixo       0.65      0.66      0.65       128
 Salário Alto       0.64      0.63      0.63       122

     accuracy                           0.64       250
    macro avg       0.64      0.64      0.64       250
 weighted avg       0.64      0.64      0.64       250


--- Importância das Features ---
                          feature  importance
19        cat__Faixa_Etaria_25-34    0.232457
0                num__Anos_Estudo    0.128308
20        cat__Faixa_Etaria_35-44    0.080058
21        cat__Faixa_Etaria_45-54    0.069047
4    cat__Atividade_Principal_2.0    0.062368
3    cat__Posição_Ocupacional_4.0    0.050990
15           cat__Regiao_Nordeste    0.049766
22          cat__Faixa_Etaria_55+    0.046616
11   cat__Atividade_Principal_9.0    0.043773
1   num__Horas_Trabalhadas_Semana    0.043658
12  cat__Atividade_Principal_10.0    0.030838
6    cat__Atividade_Principal_4.0    0.027121
17            cat__Regiao_Sudeste    0.025975
14     cat__Carteira_Assinada_2.0    0.025412
18                cat__Regiao_Sul    0.024604
------------------------------------------------------------

>>>> INICIANDO ANÁLISE DO GRUPO: NÍVEL TÉCNICO <<<<

--- Otimizando hiperparâmetros do modelo (versão original/simples)... ---
Fitting 5 folds for each of 50 candidates, totalling 250 fits

Melhor Acurácia encontrada na validação cruzada: 74.56%
Melhores Hiperparâmetros: {'classifier__subsample': 0.8, 'classifier__n_estimators': 100, 'classifier__max_depth': 3, 'classifier__learning_rate': 0.05, 'classifier__colsample_bytree': 0.8}

--- Avaliação Final no Conjunto de Teste com o Melhor Modelo ---
Resultado Acurácia Final: 68.99%
Relatório de Classificação Detalhado:
               precision    recall  f1-score   support

Salário Baixo       0.73      0.61      0.67       181
 Salário Alto       0.66      0.77      0.71       177

     accuracy                           0.69       358
    macro avg       0.70      0.69      0.69       358
 weighted avg       0.70      0.69      0.69       358


--- Importância das Features ---
                          feature  importance
14     cat__Carteira_Assinada_2.0    0.160472
15           cat__Regiao_Nordeste    0.108374
4    cat__Atividade_Principal_2.0    0.093869
0                num__Anos_Estudo    0.081083
1   num__Horas_Trabalhadas_Semana    0.070357
22          cat__Faixa_Etaria_55+    0.058150
20        cat__Faixa_Etaria_35-44    0.050278
21        cat__Faixa_Etaria_45-54    0.042991
18                cat__Regiao_Sul    0.041544
5    cat__Atividade_Principal_3.0    0.040690
2                   cat__Gênero_2    0.039060
7    cat__Atividade_Principal_5.0    0.032039
17            cat__Regiao_Sudeste    0.030535
12  cat__Atividade_Principal_10.0    0.029898
16              cat__Regiao_Norte    0.026824
------------------------------------------------------------


--- ANÁLISE COMPLETA CONCLUÍDA ---
```

