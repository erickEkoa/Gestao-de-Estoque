from gestao_ativos.banco.conexao import get_connection


def criar_tabelas():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS setores (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL UNIQUE,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS colaboradores (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            email VARCHAR(150),
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS marcas (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL UNIQUE,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS modelos (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL UNIQUE,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tipos_equipamento (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL UNIQUE,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ativos (
            id SERIAL PRIMARY KEY,
            data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            numero_serie VARCHAR(50) NOT NULL UNIQUE,
            descricao VARCHAR(255) NOT NULL,
            colaborador_id INTEGER REFERENCES colaboradores(id) ON DELETE SET NULL,
            setor_id INTEGER REFERENCES setores(id) ON DELETE SET NULL,
            status VARCHAR(50) NOT NULL,
            observacao TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id SERIAL PRIMARY KEY,
            ativo_id INTEGER NOT NULL REFERENCES ativos(id) ON DELETE CASCADE,
            data_movimentacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            tipo_movimentacao VARCHAR(50) NOT NULL,
            colaborador_id INTEGER REFERENCES colaboradores(id) ON DELETE SET NULL,
            setor_id INTEGER REFERENCES setores(id) ON DELETE SET NULL,
            status VARCHAR(50),
            observacao TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            login VARCHAR(50) NOT NULL UNIQUE,
            senha_hash VARCHAR(64) NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS anexos_ativos (
            id SERIAL PRIMARY KEY,
            ativo_id INTEGER NOT NULL REFERENCES ativos(id) ON DELETE CASCADE,
            tipo_anexo VARCHAR(100),
            nome_original VARCHAR(255) NOT NULL,
            nome_arquivo VARCHAR(255) NOT NULL,
            tipo_arquivo VARCHAR(150),
            tamanho_bytes INTEGER,
            arquivo BYTEA NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'ativos' AND column_name = 'tag_patrimonial'
            ) AND NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'ativos' AND column_name = 'numero_serie'
            ) THEN
                ALTER TABLE ativos RENAME COLUMN tag_patrimonial TO numero_serie;
            END IF;
        END $$;
    """)

    cur.execute("""
        ALTER TABLE ativos
        ADD COLUMN IF NOT EXISTS numero_serie VARCHAR(50);
    """)

    cur.execute("""
        ALTER TABLE ativos
        ADD COLUMN IF NOT EXISTS marca_id INTEGER REFERENCES marcas(id) ON DELETE SET NULL;
    """)
    cur.execute("""
        ALTER TABLE ativos
        ADD COLUMN IF NOT EXISTS modelo_id INTEGER REFERENCES modelos(id) ON DELETE SET NULL;
    """)
    cur.execute("""
        ALTER TABLE ativos
        ADD COLUMN IF NOT EXISTS tipo_equipamento_id INTEGER REFERENCES tipos_equipamento(id) ON DELETE SET NULL;
    """)

    cur.execute("""
        ALTER TABLE movimentacoes
        ADD COLUMN IF NOT EXISTS marca_id INTEGER REFERENCES marcas(id) ON DELETE SET NULL;
    """)
    cur.execute("""
        ALTER TABLE movimentacoes
        ADD COLUMN IF NOT EXISTS modelo_id INTEGER REFERENCES modelos(id) ON DELETE SET NULL;
    """)
    cur.execute("""
        ALTER TABLE movimentacoes
        ADD COLUMN IF NOT EXISTS tipo_equipamento_id INTEGER REFERENCES tipos_equipamento(id) ON DELETE SET NULL;
    """)

    cur.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'ativos' AND column_name = 'numero_serie'
            ) THEN
                BEGIN
                    ALTER TABLE ativos ALTER COLUMN numero_serie SET NOT NULL;
                EXCEPTION WHEN others THEN
                    NULL;
                END;
            END IF;
        END $$;
    """)

    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'ativos_numero_serie_key'
            ) THEN
                BEGIN
                    ALTER TABLE ativos ADD CONSTRAINT ativos_numero_serie_key UNIQUE (numero_serie);
                EXCEPTION WHEN others THEN
                    NULL;
                END;
            END IF;
        END $$;
    """)

    cur.execute("""
        ALTER TABLE anexos_ativos
        ADD COLUMN IF NOT EXISTS tipo_anexo VARCHAR(100);
    """)

    conn.commit()
    cur.close()
    conn.close()
