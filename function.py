from nomes_paises_pt import nomes_paises_pt
import json
import unicodedata


# UTILITÁRIOS BÁSICOS
def tradutor(pais: str, dicionario: dict) -> str:
    pais = pais.capitalize()
    return dicionario.get(pais, "País não encontrado no dicionário.")


def remover_acentos(texto: str) -> str:
    texto_norm = unicodedata.normalize("NFD", texto)
    return "".join(ch for ch in texto_norm if not unicodedata.combining(ch))


def montar_nome_arquivo(dado: str) -> str:
    if dado == "Desigualdade de renda":
        return "dicionario_DESIGUALDADE_RENDA.json"

    nome = dado
    if "Trabalho em " in nome:
        nome = nome.replace("Trabalho em ", "")
    elif "Trabalho " in nome:
        nome = nome.replace("Trabalho ", "")

    nome = remover_acentos(nome).upper().replace(" ", "_")
    return f"dicionario_{nome}.json"


dados_disponiveis = [
    "Desigualdade de renda",
    "Trabalho em Agricultura",
    "Trabalho em Indústria",
    "Trabalho Total",
    "PIB",
    "População",
]


def mostrar_dados_disponiveis() -> None:
    print("\nDADOS DISPONÍVEIS:")
    for i, item in enumerate(dados_disponiveis, start=1):
        print(f"{i} - {item}")
    print("-" * 40)


def escolher_dado(prompt: str) -> str | None:
    mostrar_dados_disponiveis()
    escolha = input(prompt).strip()

    if escolha.isdigit():
        idx = int(escolha) - 1
        if 0 <= idx < len(dados_disponiveis):
            return dados_disponiveis[idx]

    if escolha in dados_disponiveis:
        return escolha

    print("Dado não disponível.")
    return None


def solicitar_pais(mensagem: str = "Para qual país? ") -> tuple[str, str] | None:
    pais = input(mensagem).strip()
    en_pais = tradutor(pais, nomes_paises_pt)
    if en_pais == "País não encontrado no dicionário.":
        print(en_pais)
        return None
    return pais, en_pais


def carregar_conteudo_dado(dado: str) -> dict | None:
    arquivo = montar_nome_arquivo(dado)
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado para '{dado}'.")
        return None


def obter_info_pais(conteudo: dict, en_pais: str) -> dict | None:
    countries = conteudo.get("COUNTRIES", {})
    alvo = en_pais.strip().lower()
    for info in countries.values():
        country_name = str(info.get("country", "")).strip().lower()
        if country_name == alvo:
            return info
    return None


def obter_valores_dado_para_pais(dado: str, en_pais: str) -> dict | None:
    conteudo = carregar_conteudo_dado(dado)
    if not conteudo:
        return None

    info = obter_info_pais(conteudo, en_pais)
    if info is None:
        print(f"Não encontrei dados para o país {en_pais} em '{dado}'.")
        return None

    valores = info.get("values", {})
    if not valores:
        print(f"Não há valores numéricos em '{dado}' para {en_pais}.")
        return None

    return valores



# 1) APRESENTAR DADOS
def apresentar_dados() -> None:
    dado = escolher_dado("Escolha o número do dado que você quer ver: ")
    if not dado:
        return

    conteudo = carregar_conteudo_dado(dado)
    if conteudo is not None:
        print(conteudo)



# 2) APRESENTAR PAÍS
def apresentar_pais() -> dict | None:
    pais_en = solicitar_pais("Qual país você quer saber? ")
    if not pais_en:
        return None

    pais, en_pais = pais_en
    dados_pais: dict[str, dict | None] = {}

    for dado in dados_disponiveis:
        conteudo = carregar_conteudo_dado(dado)
        if not conteudo:
            dados_pais[dado] = None
            continue

        info = obter_info_pais(conteudo, en_pais)
        if info is None:
            dados_pais[dado] = None
            continue

        valores = {k: v for k, v in info.items() if k != "country"}
        dados_pais[dado] = {
            "link": conteudo.get("LINK"),
            "country": en_pais,
            "dados": valores,
        }

    print(dados_pais)
    return dados_pais



# 3) MÉDIA DE DADO
def calcular_media_dado() -> None:
    dado = escolher_dado("\nQual dado você quer calcular a média? (número ou nome): ")
    if not dado:
        return

    pais_en = solicitar_pais("Para qual país você quer calcular a média? ")
    if not pais_en:
        return

    pais, en_pais = pais_en
    valores = obter_valores_dado_para_pais(dado, en_pais)
    if not valores:
        return

    lista_valores = list(valores.values())
    media = sum(lista_valores) / len(lista_valores)

    print(f"\nMédia de '{dado}' para {pais} ({en_pais}) = {media}")


# 4) VARIÂNCIA DE DADO
def calcular_variancia_dado() -> None:
    dado = escolher_dado("\nQual dado você quer calcular a variância? (número ou nome): ")
    if not dado:
        return

    pais_en = solicitar_pais("Para qual país você quer calcular a variância? ")
    if not pais_en:
        return

    pais, en_pais = pais_en
    valores = obter_valores_dado_para_pais(dado, en_pais)
    if not valores:
        return

    lista_valores = list(valores.values())
    media = sum(lista_valores) / len(lista_valores)
    soma_quadrados = sum((v - media) ** 2 for v in lista_valores)
    variancia = soma_quadrados / len(lista_valores)

    print(f"\nVariância de '{dado}' para {pais} ({en_pais}) = {variancia}")


# 5) MÉDIA PONDERADA DE DADO
def calcular_media_ponderada_dado() -> None:
    dado = escolher_dado("\nQual dado você quer calcular a média ponderada? (número ou nome): ")
    if not dado:
        return

    dado_peso = escolher_dado("\nQual dado você quer usar como peso? (número ou nome): ")

    if not dado_peso:
        return

    pais_en = solicitar_pais("Para qual país você quer calcular a média ponderada? ")
    if not pais_en:
        return

    pais, en_pais = pais_en
    valores_dado = obter_valores_dado_para_pais(dado, en_pais)
    valores_peso = obter_valores_dado_para_pais(dado_peso, en_pais)

    if not valores_dado or not valores_peso:
        return

    anos_comuns = sorted(set(valores_dado.keys()) & set(valores_peso.keys()))
    if not anos_comuns:
        print("Não há anos em comum entre o dado e o dado de ponderação.")
        return

    numerador = 0.0
    denominador = 0.0

    for ano in anos_comuns:
        v = valores_dado[ano]
        p = valores_peso[ano]
        numerador += v * p
        denominador += p

    if denominador == 0:
        print("A soma dos pesos é zero. Não é possível calcular a média ponderada.")
        return

    media_pond = numerador / denominador

    print(f"\nMédia ponderada de '{dado}' para {pais} ({en_pais})\nPonderada por '{dado_peso}' = {media_pond}")


# 6) PRODUTIVIDADE x DESIGUALDADE
def calcular_produtividade_x_desigualdade() -> None:
    pais_en = solicitar_pais("Para qual país você quer calcular a produtividade x desigualdade? ")
    if not pais_en:
        return

    pais, en_pais = pais_en

    serie_pib = obter_valores_dado_para_pais("PIB", en_pais)
    serie_pop = obter_valores_dado_para_pais("População", en_pais)
    serie_trab_total = obter_valores_dado_para_pais("Trabalho Total", en_pais)
    serie_desig = obter_valores_dado_para_pais("Desigualdade de renda", en_pais)

    if not all([serie_pib, serie_pop, serie_trab_total, serie_desig]):
        print("Faltam dados para calcular a produtividade x desigualdade.")
        return

    anos_comuns = sorted(
        set(serie_pib.keys())
        & set(serie_pop.keys())
        & set(serie_trab_total.keys())
        & set(serie_desig.keys())
    )

    if not anos_comuns:
        print("Não há anos em comum entre PIB, População, Trabalho Total e Desigualdade de renda.")
        return

    resultados: dict[str, dict] = {}

    for ano in anos_comuns:
        pib = serie_pib[ano]
        pop = serie_pop[ano]
        trab_pct = serie_trab_total[ano]
        desig = serie_desig[ano]

        if pop == 0 or trab_pct == 0:
            continue

        trabalhadores = pop * trab_pct / 100.0
        produtividade = pib / trabalhadores

        resultados[ano] = {"produtividade_trabalhador": produtividade,"desigualdade_renda": desig,}

    if not resultados:
        print("Não foi possível calcular a produtividade (possíveis divisões por zero).")
        return

    print(
        f"\nProdutividade média do trabalhador x Desigualdade de renda - "
        f"{pais} ({en_pais})"
    )
    print("-" * 80)
    print(
        f"{'Ano':<6} "
        f"{'Produtividade (PIB por trabalhador)':<40} "
        f"{'Desigualdade de renda':<20}"
    )
    print("-" * 80)

    for ano in sorted(resultados.keys()):
        prod = resultados[ano]["produtividade_trabalhador"]
        desig = resultados[ano]["desigualdade_renda"]
        print(f"{ano:<6} {prod:<40} {desig:<20}")


# FLUXO USUÁRIO
def main() -> None:
    menu = (
        "\n\nDigite o número do serviço você quer utilizar:\n\n"
        "1 - Apresentar dados\n"
        "2 - Apresentar país\n"
        "3 - Calcular média de dado\n"
        "4 - Calcular variância de dado\n"
        "5 - Calcular média ponderada de dado\n"
        "6 - Produtividade média do trabalhador\n\n"
        "Se quiser sair, digite 'sair'\n\n"
        "Escolha: "
    )

    while True:
        escolha_raw = input(menu)
        escolha = escolha_raw.strip().lower()

        if escolha == "1":
            apresentar_dados()
        elif escolha == "2":
            apresentar_pais()
        elif escolha == "3":
            calcular_media_dado()
        elif escolha == "4":
            calcular_variancia_dado()
        elif escolha == "5":
            calcular_media_ponderada_dado()
        elif escolha == "6":
            calcular_produtividade_x_desigualdade()
        elif escolha == "sair":
            break
        else:
            linha = "~" * 40
            print(f"\n\n{linha}\nOpção inválida. Tente novamente.\n{linha}\n\n")


if __name__ == "__main__":
    main()
