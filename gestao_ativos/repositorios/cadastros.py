from psycopg2.extras import RealDictCursor
from gestao_ativos.banco.conexao import get_connection


def listar_setores():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome FROM setores ORDER BY nome")
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados


def inserir_setor(nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO setores (nome) VALUES (%s) ON CONFLICT (nome) DO NOTHING", (nome,))
    conn.commit()
    cur.close()
    conn.close()


def excluir_setor(setor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM setores WHERE id = %s", (setor_id,))
    conn.commit()
    cur.close()
    conn.close()


def buscar_setor_por_id(setor_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome FROM setores WHERE id = %s", (setor_id,))
    dado = cur.fetchone()
    cur.close()
    conn.close()
    return dado


def atualizar_setor(setor_id, nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE setores SET nome = %s WHERE id = %s", (nome, setor_id))
    conn.commit()
    cur.close()
    conn.close()


def listar_colaboradores():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome, email FROM colaboradores ORDER BY nome")
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados


def inserir_colaborador(nome, email=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO colaboradores (nome, email) VALUES (%s, %s)", (nome, email))
    conn.commit()
    cur.close()
    conn.close()


def excluir_colaborador(colaborador_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM colaboradores WHERE id = %s", (colaborador_id,))
    conn.commit()
    cur.close()
    conn.close()


def buscar_colaborador_por_id(colaborador_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome, email FROM colaboradores WHERE id = %s", (colaborador_id,))
    dado = cur.fetchone()
    cur.close()
    conn.close()
    return dado


def atualizar_colaborador(colaborador_id, nome, email=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE colaboradores SET nome = %s, email = %s WHERE id = %s",
        (nome, email, colaborador_id)
    )
    conn.commit()
    cur.close()
    conn.close()


def listar_marcas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome FROM marcas ORDER BY nome")
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados


def inserir_marca(nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO marcas (nome) VALUES (%s) ON CONFLICT (nome) DO NOTHING", (nome,))
    conn.commit()
    cur.close()
    conn.close()


def excluir_marca(marca_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM marcas WHERE id = %s", (marca_id,))
    conn.commit()
    cur.close()
    conn.close()


def buscar_marca_por_id(marca_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome FROM marcas WHERE id = %s", (marca_id,))
    dado = cur.fetchone()
    cur.close()
    conn.close()
    return dado


def atualizar_marca(marca_id, nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE marcas SET nome = %s WHERE id = %s", (nome, marca_id))
    conn.commit()
    cur.close()
    conn.close()


def listar_modelos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome FROM modelos ORDER BY nome")
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados


def inserir_modelo(nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO modelos (nome) VALUES (%s) ON CONFLICT (nome) DO NOTHING", (nome,))
    conn.commit()
    cur.close()
    conn.close()


def excluir_modelo(modelo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM modelos WHERE id = %s", (modelo_id,))
    conn.commit()
    cur.close()
    conn.close()


def buscar_modelo_por_id(modelo_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome FROM modelos WHERE id = %s", (modelo_id,))
    dado = cur.fetchone()
    cur.close()
    conn.close()
    return dado


def atualizar_modelo(modelo_id, nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE modelos SET nome = %s WHERE id = %s", (nome, modelo_id))
    conn.commit()
    cur.close()
    conn.close()


def listar_tipos_equipamento():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome FROM tipos_equipamento ORDER BY nome")
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados


def inserir_tipo_equipamento(nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tipos_equipamento (nome) VALUES (%s) ON CONFLICT (nome) DO NOTHING",
        (nome,)
    )
    conn.commit()
    cur.close()
    conn.close()


def excluir_tipo_equipamento(tipo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tipos_equipamento WHERE id = %s", (tipo_id,))
    conn.commit()
    cur.close()
    conn.close()


def buscar_tipo_por_id(tipo_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome FROM tipos_equipamento WHERE id = %s", (tipo_id,))
    dado = cur.fetchone()
    cur.close()
    conn.close()
    return dado


def atualizar_tipo_equipamento(tipo_id, nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tipos_equipamento SET nome = %s WHERE id = %s", (nome, tipo_id))
    conn.commit()
    cur.close()
    conn.close()
