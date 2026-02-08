# 💻 A Força de Trabalho em Tecnologia no Brasil
### Uma análise baseada em microdados públicos e Machine Learning

<div align="center">

<img 
  src="./assets/header.png" 
  alt="Força de Trabalho em Tecnologia no Brasil" 
  width="100%" 
  height="260px"
  style="object-fit: cover;"
/>

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-EC1C24?style=for-the-badge&logo=apache&logoColor=white)
![IBGE](https://img.shields.io/badge/Dados%20IBGE-PNAD%20Contínua-0066CC?style=for-the-badge)

<p align="center">
  <b>Análise quantitativa e preditiva do perfil e dos determinantes de renda dos profissionais de TI no Brasil, utilizando microdados da PNAD Contínua.</b>
</p>

<p align="center">
  📄 <a href="./artigo/SIMCADS_IA.pdf">Artigo Científico (SIMCADS)</a> • 
  🧠 <a href="./codigo">Código e Modelagem</a>
</p>

</div>

---

## 📌 Visão Geral

Este projeto investiga **quem são os profissionais de Tecnologia da Informação (TI) no Brasil** e **quais fatores mais influenciam sua renda**, a partir de **microdados oficiais do IBGE (PNAD Contínua)**.

A análise combina:

- 📊 **Estatística descritiva**
- 🧩 **Engenharia de variáveis**
- 🤖 **Modelos de Machine Learning (XGBoost)**

para comparar dois perfis distintos do mercado:

- **Profissionais de Nível Superior**
- **Profissionais de Nível Técnico / Médio**

> O estudo evidencia que o mercado de TI **não é homogêneo**:  
> os determinantes de renda variam significativamente conforme o nível de formação.

---

## 🚀 Demonstração ao Vivo

O dashboard interativo deste projeto está disponível online! Nele, você pode explorar os gráficos e as análises preditivas detalhadas por nível de formação.

👉 **[Acesse o Dashboard Aqui](link_do_seu_site_no_streamlit)**

> **Nota de Autoria:** O desenvolvimento da interface, a arquitetura web em Streamlit e a lógica de visualização de dados foram realizados integralmente por mim (**Laysa Bernardes**) como uma extensão técnica do trabalho de pesquisa original.

---

## 🔍 Principais Resultados

### 📈 Performance dos Modelos
- **Nível Superior**
  - Acurácia final: **~64%**
  - Principal fator preditivo: **Faixa Etária**
- **Nível Técnico**
  - Acurácia final: **~69%**
  - Principal fator preditivo: **Carteira Assinada (formalização)**

Esses resultados superam o desempenho aleatório (50%) e demonstram **padrões estruturais relevantes** no mercado de trabalho em TI.

---

### 🧠 Insights Relevantes

- 👩‍💻 **Nível Superior**
  - Idade (25–34 anos) tem maior impacto que escolaridade adicional
  - Mercado valoriza fase de carreira, adaptabilidade e experiência recente

- 🧑‍🔧 **Nível Técnico**
  - Formalização do vínculo empregatício é o principal divisor salarial
  - Indício de maior vulnerabilidade à informalidade

---

## 🗂 Estrutura do Repositório

```bash
.
├── artigo/              # Artigo científico (PDF)
├── codigo/              # Scripts Python e pipeline de ML
├── dados/               # Instruções e links para microdados
├── assets/              # Imagens e visualizações
└── README.md            # Visão geral (este arquivo)
```

## 📄 Publicação Acadêmica

Este trabalho foi apresentado no **2º SIMCADS — Simpósio de Análise e Desenvolvimento de Sistemas** no **IFSP — Campus Cubatão**.

> **Título:** Determinantes de Renda em TI no Brasil: uma abordagem de Machine Learning para análise de perfis por nível de formação

### 👩‍💻 Autores e Colaboradores

<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/Laysabernardes">
        <img src="https://media.licdn.com/dms/image/v2/D4D03AQHunSiEmE1sIg/profile-displayphoto-scale_400_400/B4DZpB_RKyIMAg-/0/1762043697450?e=1771459200&v=beta&t=L00Ao1xa8BnBGy-y5RV3pVgAu3kqwbV7vWPiNHR3Pq0" width="100px;" alt="Laysa Bernardes"/><br />
        <sub><b>Laysa Bernardes</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/laysabernardes/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" height="15px"/></a>
    </td>
    <td align="center">
      <a href="https://github.com/LucasLoopsT">
        <img src="https://github.com/LucasLoopsT.png" width="100px;" alt="Lucas Lopes"/><br />
        <sub><b>Lucas Lopes</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/lucaslopescruz/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" height="15px"/></a>
    </td>
    <td align="center">
      <a href="https://github.com/BeatrizBastosBorges">
        <img src="https://github.com/BeatrizBastosBorges.png" width="100px;" alt="Beatriz Bastos Borges"/><br />
        <sub><b>Beatriz Bastos</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/beatrizbastosborges/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" height="15px"/></a>
    </td>
    <td align="center">
      <a href="https://github.com/edusousax/">
        <img src="https://media.licdn.com/dms/image/v2/D4D03AQGJ6Ym2VizkQQ/profile-displayphoto-scale_400_400/B4DZhUHGEAGgAk-/0/1753757803454?e=1771459200&v=beta&t=j_zkBL9pOMFiM_fgM6xyeq0MxOZMLUfJxoZk0aD0XZI" width="100px;" alt="Eduardo Miranda"/><br />
        <sub><b>Eduardo Miranda</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/edusousax/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" height="15px"/></a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/fod0rr">
        <img src="https://media.licdn.com/dms/image/v2/D4D03AQH5dcBOxHj-EA/profile-displayphoto-scale_400_400/B4DZjISpm9HwAo-/0/1755706990467?e=1771459200&v=beta&t=jbad8BLn-vJfarTIoZpj8rjPMpev8eXVE2Ubl2ZXwrI" width="100px;" alt="Maria Eduarda Fodor"/><br />
        <sub><b>Maria E. Fodor</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/fod0rr/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" height="15px"/></a>
    </td>
    <td align="center">
      <a href="https://github.com/l3gium">
        <img src="https://github.com/l3gium.png" width="100px;" alt="Miguel Luizatto"/><br />
        <sub><b>Miguel Luizatto</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/miguel-luizatto/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" height="15px"/></a>
    </td>
    <td align="center">
      <a href="https://github.com/PedroXav">
        <img src="https://github.com/PedroXav.png" width="100px;" alt="Pedro Xavier"/><br />
        <sub><b>Pedro Xavier</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/pedro-xavier-oliveira/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" height="15px"/></a>
    </td>
    <td align="center">
      <a href="--">
        <img src="https://media.licdn.com/dms/image/v2/C4D03AQG0bUs58kfC1w/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1616441421306?e=1771459200&v=beta&t=3WMViowNTrP-x0tLqIlT9huHd2ELyWBO-TzSN7ceZnA" width="100px;" alt="Paulo Mannini"/><br />
        <sub><b>Paulo Mannini</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/paulo-mannini-pmp-psm-i-msc-itil-2681542b/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" height="15px"/></a><br />
      <sub>👨‍🏫 Orientador</sub>
    </td>
  </tr>
</table>
