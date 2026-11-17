import mimetypes
import psycopg2
from psycopg2.extras import RealDictCursor
from gestao_ativos.banco.conexao import get_connection
from gestao_ativos.util import normalizar_nome_arquivo


def adicionar_anexo_ao_ativo(ativo_id, arquivo_storage, tipo_anexo=None):
    if not arquivo_storage or not arquivo_storage.filename:
        return

    nome_original = arquivo_storage.filename.strip()
    if not nome_original:
        return

    nome_arquivo = normalizar_nome_arquivo(nome_original)
    conteudo = arquivo_storage.read()
    if not conteudo:
        raise ValueError(f"O arquivo '{nome_original}' está vazio.")

    tipo_arquivo = arquivo_storage.mimetype or mimetypes.guess_type(nome_original)[0] or "application/octet-stream"
    tamanho_bytes = len(conteudo)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO anexos_ativos (
            ativo_id, tipo_anexo, nome_original, nome_arquivo, tipo_arquivo, tamanho_bytes, arquivo
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (ativo_id, (tipo_anexo or '').strip() or None, nome_original, nome_arquivo, tipo_arquivo, tamanho_bytes, psycopg2.Binary(conteudo))
    )
    conn.commit()
    cur.close()
    conn.close()


def listar_anexos_do_ativo(ativo_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT
            id,
            ativo_id,
            tipo_anexo,
            nome_original,
            nome_arquivo,
            tipo_arquivo,
            tamanho_bytes,
            TO_CHAR(criado_em, 'DD/MM/YYYY HH24:MI:SS') AS criado_em
        FROM anexos_ativos
        WHERE ativo_id = %s
        ORDER BY id DESC
        """,
        (ativo_id,)
    )
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados


def buscar_anexo_por_id(anexo_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT
            id,
            ativo_id,
            tipo_anexo,
            tipo_anexo,
            nome_original,
            nome_arquivo,
            tipo_arquivo,
            tamanho_bytes,
            arquivo
        FROM anexos_ativos
        WHERE id = %s
        """,
        (anexo_id,)
    )
    dado = cur.fetchone()
    cur.close()
    conn.close()
    return dado


def excluir_anexo(anexo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM anexos_ativos WHERE id = %s", (anexo_id,))
    conn.commit()
    cur.close()
    conn.close()
