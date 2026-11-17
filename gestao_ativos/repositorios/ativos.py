import mimetypes
import psycopg2
from psycopg2.extras import RealDictCursor
from gestao_ativos.banco.conexao import get_connection
from gestao_ativos.util import normalizar_nome_arquivo


def cadastrar_ativo(numero_serie, descricao, colaborador_id, setor_id, marca_id, modelo_id, tipo_equipamento_id, status, observacao, anexos=None, tipo_anexo=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM ativos WHERE numero_serie = %s", (numero_serie,))
    existe = cur.fetchone()
    if existe:
        cur.close()
        conn.close()
        raise ValueError(f"O número de série '{numero_serie}' já está cadastrado.")

    cur.execute(
        """
        INSERT INTO ativos (
            numero_serie, descricao, colaborador_id, setor_id,
            marca_id, modelo_id, tipo_equipamento_id, status, observacao
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            numero_serie, descricao, colaborador_id, setor_id,
            marca_id, modelo_id, tipo_equipamento_id, status, observacao
        )
    )
    ativo_id = cur.fetchone()[0]

    cur.execute(
        """
        INSERT INTO movimentacoes (
            ativo_id, tipo_movimentacao, colaborador_id, setor_id,
            marca_id, modelo_id, tipo_equipamento_id, status, observacao
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            ativo_id, "CADASTRO", colaborador_id, setor_id,
            marca_id, modelo_id, tipo_equipamento_id, status,
            "Cadastro inicial do ativo"
        )
    )

    if anexos:
        for arquivo in anexos:
            if arquivo and arquivo.filename:
                nome_original = arquivo.filename.strip()
                if not nome_original:
                    continue
                nome_arquivo = normalizar_nome_arquivo(nome_original)
                conteudo = arquivo.read()
                if not conteudo:
                    continue
                tipo_arquivo = arquivo.mimetype or mimetypes.guess_type(nome_original)[0] or "application/octet-stream"
                tamanho_bytes = len(conteudo)
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


def buscar_ativos(filtro_numero_serie="", filtro_modelo="", filtro_colaborador="", filtro_tipo=""):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
        SELECT
            a.id,
            TO_CHAR(a.data_cadastro, 'DD/MM/YYYY HH24:MI:SS') AS data_cadastro,
            a.numero_serie,
            a.descricao,
            COALESCE(c.nome, '') AS colaborador,
            COALESCE(s.nome, '') AS setor,
            COALESCE(m.nome, '') AS marca,
            COALESCE(md.nome, '') AS modelo,
            COALESCE(te.nome, '') AS tipo_equipamento,
            a.status,
            COALESCE(a.observacao, '') AS observacao,
            COUNT(ax.id) AS total_anexos
        FROM ativos a
        LEFT JOIN colaboradores c ON c.id = a.colaborador_id
        LEFT JOIN setores s ON s.id = a.setor_id
        LEFT JOIN marcas m ON m.id = a.marca_id
        LEFT JOIN modelos md ON md.id = a.modelo_id
        LEFT JOIN tipos_equipamento te ON te.id = a.tipo_equipamento_id
        LEFT JOIN anexos_ativos ax ON ax.ativo_id = a.id
        WHERE
            (%s = '' OR a.numero_serie ILIKE %s)
            AND (%s = '' OR md.nome ILIKE %s)
            AND (%s = '' OR c.nome ILIKE %s)
            AND (%s = '' OR te.nome ILIKE %s)
        GROUP BY a.id, c.nome, s.nome, m.nome, md.nome, te.nome
        ORDER BY a.id DESC
    """

    cur.execute(sql, (
        filtro_numero_serie, f"%{filtro_numero_serie}%",
        filtro_modelo, f"%{filtro_modelo}%",
        filtro_colaborador, f"%{filtro_colaborador}%",
        filtro_tipo, f"%{filtro_tipo}%"
    ))

    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados


def buscar_ativo_por_id(ativo_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT
            a.id,
            a.numero_serie,
            a.descricao,
            a.colaborador_id,
            a.setor_id,
            a.marca_id,
            a.modelo_id,
            a.tipo_equipamento_id,
            a.status,
            COALESCE(a.observacao, '') AS observacao,
            COUNT(ax.id) AS total_anexos
        FROM ativos a
        LEFT JOIN anexos_ativos ax
            ON ax.ativo_id = a.id
        WHERE a.id = %s
        GROUP BY
            a.id,
            a.numero_serie,
            a.descricao,
            a.colaborador_id,
            a.setor_id,
            a.marca_id,
            a.modelo_id,
            a.tipo_equipamento_id,
            a.status,
            a.observacao
        """,
        (ativo_id,)
    )

    dado = cur.fetchone()

    cur.close()
    conn.close()

    return dado


def atualizar_ativo(ativo_id, numero_serie, descricao, colaborador_id, setor_id, marca_id, modelo_id, tipo_equipamento_id, status, observacao):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id FROM ativos
        WHERE numero_serie = %s AND id <> %s
        """,
        (numero_serie, ativo_id)
    )
    existe = cur.fetchone()
    if existe:
        cur.close()
        conn.close()
        raise ValueError(f"O número de série '{numero_serie}' já está cadastrado em outro ativo.")

    cur.execute(
        """
        UPDATE ativos
        SET numero_serie = %s,
            descricao = %s,
            colaborador_id = %s,
            setor_id = %s,
            marca_id = %s,
            modelo_id = %s,
            tipo_equipamento_id = %s,
            status = %s,
            observacao = %s
        WHERE id = %s
        """,
        (
            numero_serie, descricao, colaborador_id, setor_id,
            marca_id, modelo_id, tipo_equipamento_id, status, observacao, ativo_id
        )
    )

    cur.execute(
        """
        INSERT INTO movimentacoes (
            ativo_id, tipo_movimentacao, colaborador_id, setor_id,
            marca_id, modelo_id, tipo_equipamento_id, status, observacao
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            ativo_id, "ATUALIZACAO", colaborador_id, setor_id,
            marca_id, modelo_id, tipo_equipamento_id, status,
            observacao or "Atualização do ativo"
        )
    )

    conn.commit()
    cur.close()
    conn.close()


def excluir_ativo(ativo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ativos WHERE id = %s", (ativo_id,))
    conn.commit()
    cur.close()
    conn.close()
