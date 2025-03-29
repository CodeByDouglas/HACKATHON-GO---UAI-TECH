import sqlite3
import os

# Define o caminho para o arquivo do banco de dados
CAMINHO_BD = os.path.join(os.path.dirname(__file__), "sessao.db")

# Estabelece a conexão com o banco SQLite
# O parâmetro check_same_thread=False permite acesso de múltiplas threads (use com cautela em produção)
conexao = sqlite3.connect(CAMINHO_BD, check_same_thread=False)
cursor = conexao.cursor()

# Cria a tabela 'sessoes' se ela não existir, com apenas dois campos:
# - numero_usuario (chave primária)
# - etapa (etapa atual da sessão)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessoes (
        numero_usuario TEXT PRIMARY KEY,
        etapa TEXT,
        cep TEXT
    )
''')
conexao.commit()

def iniciar_sessao(numero_usuario):
    """
    Inicia uma nova sessão para o usuário com a etapa inicial.
    """
    etapa = "incerir_cep"  # Defina a etapa inicial desejada
    cursor.execute('''
        INSERT OR REPLACE INTO sessoes (numero_usuario, etapa)
        VALUES (?, ?)
    ''', (numero_usuario, etapa))
    conexao.commit()

def atualizar_etapa(numero_usuario, etapa):
    """
    Atualiza a etapa atual da sessão do usuário.
    """
    cursor.execute('UPDATE sessoes SET etapa=? WHERE numero_usuario=?', (etapa, numero_usuario))
    conexao.commit()
    
def atualizar_cep(numero_usuario, cep):
    """
    Atualiza a etapa atual da sessão do usuário.
    """
    cursor.execute('UPDATE sessoes SET cep=? WHERE numero_usuario=?', (cep, numero_usuario))
    conexao.commit()

def fechar_sessao(numero_usuario):
    """
    Remove a sessão do usuário do banco de dados.
    """
    cursor.execute('DELETE FROM sessoes WHERE numero_usuario=?', (numero_usuario,))
    conexao.commit()

def obter_sessao(numero_usuario):
    """
    Retorna a etapa da sessão do usuário, se existir.
    """
    cursor.execute('SELECT etapa FROM sessoes WHERE numero_usuario=?', (numero_usuario,))
    linha = cursor.fetchone()
    if linha:
        (etapa,) = linha
        return etapa
    return None

def obter_cep(numero_usuario):
    """
    Retorna o CEP da sessão do usuário, se existir.
    """
    cursor.execute('SELECT cep FROM sessoes WHERE numero_usuario=?', (numero_usuario,))
    linha = cursor.fetchone()
    if linha:
        (cep,) = linha
        return cep
    return None

