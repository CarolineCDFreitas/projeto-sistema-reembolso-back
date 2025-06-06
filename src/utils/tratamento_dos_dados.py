import re
from decimal import Decimal
from marshmallow import ValidationError

def tratamento_dos_dados(dados: dict):
    
    for campo, valor in dados.items():
        if isinstance(valor, str):
            dados[campo] = valor.strip()
        
        
    campos_opcionais = ["ordemInterna", "divisao", "pep", "distKm", "valorKm"]

    for campo in campos_opcionais:
        valor = dados.get(campo)
        if valor == "":
            dados[campo] = None
        
        elif (campo == "distKm" and valor is not None):
            if not re.match(r"^\d{1,5}$", valor):
                raise ValidationError({campo: "Somente números (máx. 5 dígitos)"})
            else:
                dados[campo] = int(valor)
                
        elif (campo == "valorKm" and valor is not None):
            if not re.match(r"^\d{0,8}\.\d{2}$", valor):
                raise ValidationError({campo: "Use o formato 00.00"})
            else: 
                dados[campo] = Decimal(valor)
        

    dados_decimals = ["valorFaturado", "despesaTotal"]
    
    for campo in dados_decimals:
        valor = dados.get(campo)
        if valor:
            if not re.match(r"^\d{0,8}\.\d{2}$", valor):
                raise ValidationError({campo: "Use o formato 00.00"})
            else:
                dados[campo] = Decimal(valor)
        
    return dados
