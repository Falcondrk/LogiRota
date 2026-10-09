"""Camada de persistencia SQLite do LogiRota (Semana 1)."""
import sqlite3
from pathlib import Path

# O banco fica na pasta raiz do projeto, independentemente da pasta atual do terminal.
CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "logirota.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS pontos (
    nome TEXT PRIMARY KEY,
    bairro TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS ruas (
    origem TEXT NOT NULL REFERENCES pontos(nome),
    destino TEXT NOT NULL REFERENCES pontos(nome),
    PRIMARY KEY (origem, destino)
);
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destino TEXT NOT NULL REFERENCES pontos(nome),
    status TEXT NOT NULL DEFAULT 'pendente'
);
CREATE TABLE IF NOT EXISTS rotas_calculadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origem TEXT NOT NULL,
    sequencia TEXT NOT NULL,
    distancia_total REAL NOT NULL,
    criada_em TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def inicializar():
    """Cria as tabelas caso ainda nao existam."""
    with conectar() as conexao:
        conexao.executescript(SCHEMA)

def salvar_ponto(ponto):
    """Salva um ponto; se o nome ja existe, nao duplica nem sobrescreve."""
    with conectar() as conexao:
        conexao.execute(
            "INSERT OR IGNORE INTO pontos (nome, bairro, x, y) VALUES (?, ?, ?, ?)",
            (ponto[0], ponto[1], ponto[2], ponto[3]),
        )

def salvar_rua(origem, destino):
    """Salva a rua sem duplicar. A rua e nao direcionada no grafo."""
    with conectar() as conexao:
        conexao.execute(
            "INSERT OR IGNORE INTO ruas (origem, destino) VALUES (?, ?)",
            (origem, destino),
        )
        conexao.execute(
            "INSERT OR IGNORE INTO ruas (origem, destino) VALUES (?, ?)",
            (destino, origem),
        )

def salvar_pedido(destino):
    """Cadastra um pedido pendente para um ponto existente."""
    with conectar() as conexao:
        cursor = conexao.execute(
            "INSERT INTO pedidos (destino) VALUES (?)", (destino,)
        )
        return cursor.lastrowid

def listar_pontos():
    with conectar() as conexao:
        return conexao.execute(
            "SELECT nome, bairro, x, y FROM pontos ORDER BY nome"
        ).fetchall()

def listar_ruas():
    with conectar() as conexao:
        return conexao.execute(
            "SELECT origem, destino FROM ruas WHERE origem < destino ORDER BY origem, destino"
        ).fetchall()

def listar_pedidos_pendentes():
    with conectar() as conexao:
        return conexao.execute(
            "SELECT id, destino, status FROM pedidos WHERE status = 'pendente' ORDER BY id"
        ).fetchall()

def quantidade_pontos():
    with conectar() as conexao:
        return conexao.execute("SELECT COUNT(*) FROM pontos").fetchone()[0]
