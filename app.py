from gestao_ativos import create_app
from gestao_ativos.config import DB_CONFIG
from gestao_ativos.banco.esquema import criar_tabelas
from gestao_ativos.repositorios.usuarios import criar_usuario_padrao


app = create_app()


if __name__ == "__main__":
    if not app.secret_key or not DB_CONFIG["password"]:
        raise SystemExit("Preencha ATIVOS_SECRET_KEY e ATIVOS_DB_PASSWORD no arquivo .env.")

    criar_tabelas()
    criar_usuario_padrao()
    app.run(host="0.0.0.0", port=5000)
