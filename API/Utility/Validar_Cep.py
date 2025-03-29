import re

def cep_valido(cep: str) -> bool:
    """
    Verifica se o CEP é válido. O CEP é considerado válido se estiver no formato:
    - NNNNN-NNN ou
    - NNNNNNNN
    Onde N é um dígito.
    
    Retorna True se for válido, False caso contrário.
    """
    # Define o padrão para os dois formatos aceitos
    padrao = r'^\d{5}-\d{3}$|^\d{8}$'
    return bool(re.match(padrao, cep))

# Exemplos de uso:
print(cep_valido("74250-010"))  # True
print(cep_valido("74250010"))   # True
print(cep_valido("74250-01"))   # False
print(cep_valido("74A50-010"))  # False
