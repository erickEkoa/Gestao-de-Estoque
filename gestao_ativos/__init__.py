import os
from gestao_ativos.config import SECRET_KEY
from flask import Flask

from gestao_ativos.rotas import anexos, ativos, auth, cadastros, dashboard, exportacao


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    )

    for modulo in (auth, dashboard, ativos, cadastros, anexos, exportacao):
        modulo.registrar_rotas(app)

    return app
