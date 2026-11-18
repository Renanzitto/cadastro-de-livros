import sqlite3
from pathlib import Path

# Localização do banco de dados
CAMINHO_BANCO = Path(__file__).parent / "biblioteca.db"


# Cria a conexão com o banco
def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


# Cria a tabela de livros
def criar_tabela():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


# Cadastra um livro
def cadastrar_livro(titulo, autor, ano):
    conexao = conectar()

    cursor = conexao.execute("""
        INSERT INTO livros (titulo, autor, ano)
        VALUES (?, ?, ?)
    """, (titulo, autor, ano))

    conexao.commit()
    livro_id = cursor.lastrowid
    conexao.close()

    return livro_id


# Lista todos os livros
def listar_livros():
    conexao = conectar()

    livros = conexao.execute("""
        SELECT * FROM livros ORDER BY id DESC
    """).fetchall()

    conexao.close()

    return [dict(livro) for livro in livros]


# Exclui um livro pelo ID
def excluir_livro(livro_id):
    conexao = conectar()

    cursor = conexao.execute("""
        DELETE FROM livros WHERE id = ?
    """, (livro_id,))

    conexao.commit()
    excluido = cursor.rowcount > 0
    conexao.close()

    return excluido