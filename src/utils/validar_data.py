from datetime import date
from marshmallow import ValidationError

def validar_data(data):
    if (data > date.today()):
        raise ValidationError ("A data não pode ser no futuro")