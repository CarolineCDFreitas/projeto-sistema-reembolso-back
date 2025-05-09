def limpeza_de_dados(dados):
    campos_opcionais = ["ordemInterna", "divisao", "pep", "distKm", "valorKm"]

    for campo in campos_opcionais:
        if dados.get(campo) == "":
            dados[campo] = None

    return dados
