import os
from psycopg2.extras import RealDictCursor
from gestao_ativos.banco.conexao import get_connection
from gestao_ativos.util import gerar_hash_senha


def criar_usuario_padrao():
    senha_inicial = os.getenv("ATIVOS_ADMIN_PASSWORD")
    if not senha_inicial:
        return

    conn = get_connection()
    cur = conn.cursor()
    login_padrao = "admin"
    senha_padrao = gerar_hash_senha(senha_inicial)

    cur.execute("SELECT id FROM usuarios WHERE login = %s", (login_padrao,))
    existe = cur.fetchone()

    if not existe:
        cur.execute(
            """
            INSERT INTO usuarios (nome, login, senha_hash, ativo)
            VALUES (%s, %s, %s, %s)
            """,
            ("Administrador", login_padrao, senha_padrao, True)
        )
        conn.commit()

    cur.close()
    conn.close()


def validar_login(login, senha):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    senha_hash = gerar_hash_senha(senha)

    cur.execute(
        """
        SELECT id, nome, login
        FROM usuarios
        WHERE login = %s AND senha_hash = %s AND ativo = TRUE
        """,
        (login, senha_hash)
    )
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return usuario
