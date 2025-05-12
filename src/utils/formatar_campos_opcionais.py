def formatar_campos_opcionais(reembolso):
    campos_opcionais = ["ordemInterna", "divisao", "pep", "distKm", "valorKm"]

    for campo in campos_opcionais:
        if campo in reembolso and reembolso[campo] is None:
            reembolso[campo] = "—"

    return reembolso
