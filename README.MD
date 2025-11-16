Ana Luiza Tibiriçá da Paixão - RM562098
Luara Martins de Oliveira Ramos - RM565573

============================================

Os dados utilizados neste trabalho foram extraídos por meio da API do World Bank Group (WBG), organismo internacional composto por instituições financeiras e agências de desenvolvimento que apoiam países de baixa e média renda na promoção do crescimento econômico e na redução da pobreza, disponibilizando indicadores socioeconômicos padronizados para análise comparativa entre países.

https://www.worldbank.org/ext/en/home

De acordo com a lógica descrita a seguir:

"

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

with open("ARQUIVO JSON AQUI", "w", encoding="utf-8") as f:
    json.dump(gdp_dict, f, ensure_ascii=False, indent=2)