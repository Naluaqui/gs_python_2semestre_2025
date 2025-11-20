# Coleta de Indicadores Socioeconômicos via World Bank API

## Autores

- Ana Luiza Tibiriçá da Paixão – RM562098  
- Luara Martins de Oliveira Ramos – RM565573  

---

## Contexto

Este repositório faz parte do projeto de Graduação em Engenharia de Software (2º semestre de 2025), com foco em análise de indicadores de trabalho, renda e produtividade a partir de dados do **World Bank Group (WBG)**.

O objetivo é:

- extrair indicadores socioeconômicos padronizados por país e ano;
- organizar esses dados em arquivos JSON;
- permitir cálculos estatísticos simples (média, variância, média ponderada);
- criar um indicador derivado de **produtividade média do trabalhador** e relacioná-lo com a **desigualdade de renda**.

---

## Descrição do projeto

O projeto utiliza a **API do World Bank Group (WBG)**, organismo internacional que apoia países de baixa e média renda na promoção do crescimento econômico e na redução da pobreza.

A partir da API, são obtidos dados:

- **padronizados por país (código ISO3)**  
- **organizados por ano**

Isso permite análises comparativas entre diferentes países e períodos.

- Site oficial do WBG:  
  <https://www.worldbank.org/ext/en/home>

---

## Indicadores utilizados

Os principais indicadores extraídos e utilizados são:

- **Desigualdade de renda**  (`SI.POV.GINI`) 
  Medida de concentração de renda no país (ex.: índice de Gini ou indicador equivalente).

- **Trabalho em Agricultura (%)**  (`SL.AGR.EMPL.ZS`) 
  Proporção da força de trabalho empregada na agricultura.

- **Trabalho em Indústria (%)**  (`SL.IND.EMPL.ZS`) 
  Proporção da força de trabalho empregada na indústria.

- **Trabalho Total em Serviços (%)**  (`SL.SRV.EMPL.ZS`) 
  Proporção da força de trabalho empregada em serviços.

- **PIB (US$ corrente)** (`NY.GDP.MKTP.CD`)  
  Tamanho da economia em dólares correntes.

- **População total** (`SP.POP.TOTL`)  
  Número total de habitantes.

Esses indicadores são combinados para estudar estrutura do mercado de trabalho, tamanho da economia e desigualdade de renda.

---

## Estrutura do projeto

Principais arquivos do repositório:

- `main.py`  
  Script principal interativo (menu com opções para exibir dados e fazer cálculos).

- `nomes_paises_pt.py`  
  Dicionário/mapeamento de nomes de países em português → inglês, usado pela função `tradutor()`.

- `dicionario_PIB.json`  
  Dados de PIB por país e ano.

- `dicionario_População.json`  
  Dados de população total por país e ano.

- `dicionario_Trabalho_Total.json`  
  Percentual da população ocupada em serviços.

- `dicionario_Trabalho_Agricultura.json`  
  Percentual da população ocupada em agricultura.

- `dicionario_Trabalho_Industria.json`  
  Percentual da população ocupada em indústria.

- `dicionario_DESIGUALDADE_RENDA.json`  
  Indicador de desigualdade de renda por país e ano.

> Os nomes exatos dos arquivos podem variar levemente, mas seguem esse padrão.

---

## Requisitos

- **Python** instalado na máquina.

---

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/Naluaqui/gs_python_2semestre_2025.git
```

### 2. Acessar a pasta do projeto

```bash
cd gs_python_2semestre_2025
```

### 3. Executar o script principal

```bash
python main.py
```

O programa será iniciado no terminal e você poderá interagir com as opções disponíveis.

---

## Funcionalidades do programa

Ao executar `python main.py`, o menu oferece as seguintes opções:

### 1. Apresentar dados
Exibe o conteúdo bruto de um indicador (arquivo JSON escolhido pelo usuário).

### 2. Apresentar país
Mostra, em formato de dicionário, todos os indicadores disponíveis para um determinado país, usando a função `tradutor()` para mapear o nome do país em português para inglês.

### 3. Calcular média de dado
Calcula a média temporal de um indicador para um país (por exemplo, PIB médio ou percentual médio de trabalho em agricultura).

### 4. Calcular variância de dado
Retorna a variância dos valores do indicador ao longo dos anos para um país específico.

### 5. Calcular média ponderada de dado
Calcula uma média ponderada de um indicador usando outro como peso (por exemplo, ponderar um indicador pela população ou pelo PIB).

### 6. Produtividade média do trabalhador × Desigualdade de renda

Esta opção:

1. **Estima o número de trabalhadores:**

   ```text
   Trabalhadores ≈ População × (Trabalho Total (%) / 100)
   ```

2. **Calcula a produtividade média do trabalhador:**

  ```text
  Produtividade = PIB / Trabalhadores
  ```


3. **Relaciona esse valor de produtividade com o indicador de Desigualdade de renda para os mesmos anos, permitindo comparar nível de produtividade e nível de desigualdade ao longo do tempo.**

  ```text
  ::contentReference[oaicite:0]{index=0}
  ```
