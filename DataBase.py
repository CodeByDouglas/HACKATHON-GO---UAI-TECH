import sqlite3

# Conecta (ou cria) o banco de dados chamado "coletas.db"
conexao = sqlite3.connect("DataBase.db")
cursor = conexao.cursor()

conexao.close()

print("Banco de dados e tabelas criados com sucesso!")
