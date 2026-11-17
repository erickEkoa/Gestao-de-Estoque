from flask import render_template
from gestao_ativos.auth import login_required
from gestao_ativos.repositorios.ativos import buscar_ativos
from gestao_ativos.repositorios.cadastros import listar_colaboradores, listar_setores


@login_required
def dashboard():
    ativos_lista = buscar_ativos()
    return render_template(
        "dashboard/index.html",
        title="Dashboard",
        ativos_lista=ativos_lista,
        total_colaboradores=len(listar_colaboradores()),
        total_setores=len(listar_setores()),
    )


def registrar_rotas(app):
    app.add_url_rule("/dashboard", view_func=dashboard)
