import sqlite3

def consultar_coleta_organica(cep_str):
    """
    Consulta a tabela Coleta_Organica para verificar se o CEP informado se encontra
    dentro de algum intervalo cadastrado. Se sim, retorna o período de coleta; caso contrário,
    retorna uma mensagem informando que o CEP não está registrado.

    Parâmetro:
        cep_str (str): CEP no formato "NNNNN-NNN" ou "NNNNNNNN".
    
    Retorna:
        str: Período de coleta ou mensagem de CEP não registrado.
    """
    # Remove hífen e converte o CEP para inteiro
    try:
        cep_int = int(cep_str.replace("-", ""))
    except ValueError:
        return "CEP inválido"

    # Conecta ao banco de dados (altere o nome do arquivo conforme necessário)
    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    # Consulta os intervalos de CEP na tabela Coleta_Organica
    query = """
        SELECT periodo_de_coleta
        FROM Coleta_Organica
        WHERE ? BETWEEN cep_inicial AND cep_final
        LIMIT 1
    """
    cursor.execute(query, (cep_int,))
    resultado = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Se encontrou um resultado, retorna o período; caso contrário, informa que não está registrado
    if resultado:
        return resultado[0]
    else:
        return "Ainda não temos esse CEP registrado. 😟"

# Exemplo de uso:
cep_input = "74461295"
print(consultar_coleta_organica(cep_input))


import sqlite3

def consultar_coleta_seletiva(cep_str):
    """
    Consulta a tabela Coleta_Seletiva para verificar se o CEP informado se encontra
    dentro de algum intervalo cadastrado. Se sim, retorna o período de coleta; caso contrário,
    retorna uma mensagem informando que o CEP não está registrado.

    Parâmetro:
        cep_str (str): CEP no formato "NNNNN-NNN" ou "NNNNNNNN".
    
    Retorna:
        str: Período de coleta ou mensagem de CEP não registrado.
    """
    # Remove hífen e converte o CEP para inteiro
    try:
        cep_int = int(cep_str.replace("-", ""))
    except ValueError:
        return "CEP inválido"

    # Conecta ao banco de dados (altere o nome do arquivo conforme necessário)
    conexao = sqlite3.connect("DataBase.db")
    cursor = conexao.cursor()

    # Consulta os intervalos de CEP na tabela Coleta_Organica
    query = """
        SELECT periodo_de_coleta
        FROM Coleta_Seletiva
        WHERE ? BETWEEN cep_inicial AND cep_final
        LIMIT 1
    """
    cursor.execute(query, (cep_int,))
    resultado = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Se encontrou um resultado, retorna o período; caso contrário, informa que não está registrado
    if resultado:
        return resultado[0]
    else:
        return "Ainda não temos esse CEP registrado. 😟"

# Exemplo de uso:
cep_input = "74461295"
print(consultar_coleta_organica(cep_input))
