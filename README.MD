# Coleta de Indicadores Socioeconômicos via World Bank API

## Autores

- Ana Luiza Tibiriçá da Paixão – RM562098  
- Luara Martins de Oliveira Ramos – RM565573  

---

## Descrição

Este projeto realiza a extração de indicadores socioeconômicos fornecidos pela **API do World Bank Group (WBG)**, um organismo internacional composto por instituições financeiras e agências de desenvolvimento que apoiam países de baixa e média renda na promoção do crescimento econômico e redução da pobreza.

A partir da API, são obtidos dados **padronizados por país e ano**, permitindo análises comparativas entre diferentes regiões do mundo.

- Site oficial do WBG:  
  <https://www.worldbank.org/ext/en/home>

---

## Como o script funciona

1. Define o **indicador** desejado (por exemplo, PIB, população, emprego em agricultura etc.).
2. Faz requisições paginadas à API do World Bank para **todos os países**.
3. Para cada registro, extrai:
   - Código do país (ISO3)  
   - Nome do país  
   - Ano  
   - Valor do indicador
4. Organiza os dados em um dicionário Python no formato:

   ```json
   {
     "BRA": {
       "country": "Brazil",
       "values": {
         "2023": 12345.67,
         "2022": 12000.00
       }
     },
     "ARG": {
       "country": "Argentina",
       "values": {
         "2023": 9876.54
       }
     }
   }

5.Salva o resultado em um arquivo **JSON** com codificação **UTF-8**.

### Código utilizado

```python
import requests
import json

INDICATOR = "INDICADOR AQUI"
BASE_URL = f"https://api.worldbank.org/v2/country/all/indicator/{INDICATOR}"

params = {
    "format": "json",
    "per_page": 20000,
    "page": 1,
}

resp = requests.get(BASE_URL, params=params)
resp.raise_for_status()
data = resp.json()

meta = data[0]
total_pages = meta["pages"]

gdp_dict = {}

for page in range(1, total_pages + 1):
    params["page"] = page
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    data = resp.json()

    registros = data[1]

    for item in registros:
        iso3 = item.get("countryiso3code")
        if not iso3:
            continue

        country_name = item["country"]["value"]
        year = int(item["date"])
        value = item["value"]

        if iso3 not in gdp_dict:
            gdp_dict[iso3] = {
                "country": country_name,
                "values": {}
            }

        if value is not None:
            gdp_dict[iso3]["values"][year] = value

with open("ARQUIVO_JSON_AQUI.json", "w", encoding="utf-8") as f:
    json.dump(gdp_dict, f, ensure_ascii=False, indent=2)
```

## Como usar

1. **Instale as dependências:**

   ```bash
   pip install requests
```

2.Escolha o indicador do World Bank e substitua em:

```python
INDICATOR = "INDICADOR AQUI"
```

**Exemplos de indicadores:**

- PIB (US$ corrente): `NY.GDP.MKTP.CD`
- População total: `SP.POP.TOTL`
- Emprego na agricultura (%): `SL.AGR.EMPL.ZS`

3.Defina o nome do arquivo de saída:

```python
with open("ARQUIVO_JSON_AQUI.json", "w", encoding="utf-8") as f:
...

4.Execute o script:

```bash
python nome_do_arquivo.py
```

5.O arquivo **JSON** gerado poderá ser utilizado nas análises do trabalho, por exemplo para:

- cálculo de médias;
- cálculo de variâncias;
- estimativa de produtividade média do trabalhador;
- comparação de indicadores entre países e ao longo do tempo.

Esses dados servem como base para diferentes explorações estatísticas e visualizações no contexto do projeto.



