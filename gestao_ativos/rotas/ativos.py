from flask import flash, redirect, render_template, request, url_for
from gestao_ativos.auth import login_required
from gestao_ativos.repositorios.anexos import adicionar_anexo_ao_ativo, listar_anexos_do_ativo
from gestao_ativos.repositorios.ativos import (
    atualizar_ativo,
    buscar_ativo_por_id,
    buscar_ativos,
    cadastrar_ativo,
    excluir_ativo,
)
from gestao_ativos.repositorios.cadastros import (
    listar_colaboradores,
    listar_marcas,
    listar_modelos,
    listar_setores,
    listar_tipos_equipamento,
)
from gestao_ativos.util import to_int_or_none


@login_required
def ativos():
    if request.method == "POST":
        try:
            cadastrar_ativo(
                request.form.get("numero_serie", "").strip(),
                request.form.get("descricao", "").strip(),
                to_int_or_none(request.form.get("colaborador_id")),
                to_int_or_none(request.form.get("setor_id")),
                to_int_or_none(request.form.get("marca_id")),
                to_int_or_none(request.form.get("modelo_id")),
                to_int_or_none(request.form.get("tipo_equipamento_id")),
                request.form.get("status", "Em uso").strip(),
                request.form.get("observacao", "").strip(),
                request.files.getlist("anexos"),
                request.form.get("tipo_anexo", "").strip(),
            )
            flash("Ativo cadastrado com sucesso.", "success")
        except Exception as e:
            flash(f"Erro ao cadastrar ativo: {e}", "error")
        return redirect(url_for("ativos"))

    filtro_numero_serie = request.args.get("numero_serie", "").strip()
    filtro_modelo = request.args.get("modelo", "").strip()
    filtro_colaborador = request.args.get("colaborador", "").strip()
    filtro_tipo = request.args.get("tipo", "").strip()

    dados = buscar_ativos(filtro_numero_serie, filtro_modelo, filtro_colaborador, filtro_tipo)
    colaboradores = listar_colaboradores()
    setores = listar_setores()
    marcas = listar_marcas()
    modelos = listar_modelos()
    tipos = listar_tipos_equipamento()

    return render_template(
        "ativos/index.html",
        title="Ativos",
        dados=dados,
        colaboradores=colaboradores,
        setores=setores,
        marcas=marcas,
        modelos=modelos,
        tipos=tipos,
        filtro_numero_serie=filtro_numero_serie,
        filtro_modelo=filtro_modelo,
        filtro_colaborador=filtro_colaborador,
        filtro_tipo=filtro_tipo,
    )


@login_required
def editar_ativo_web(ativo_id):
    ativo = buscar_ativo_por_id(ativo_id)
    if not ativo:
        flash("Ativo não encontrado.", "error")
        return redirect(url_for("ativos"))

    if request.method == "POST":
        try:
            atualizar_ativo(
                ativo_id,
                request.form.get("numero_serie", "").strip(),
                request.form.get("descricao", "").strip(),
                to_int_or_none(request.form.get("colaborador_id")),
                to_int_or_none(request.form.get("setor_id")),
                to_int_or_none(request.form.get("marca_id")),
                to_int_or_none(request.form.get("modelo_id")),
                to_int_or_none(request.form.get("tipo_equipamento_id")),
                request.form.get("status", "Em uso").strip(),
                request.form.get("observacao", "").strip(),
            )

            tipo_anexo = request.form.get("tipo_anexo", "").strip()
            for arquivo in request.files.getlist("anexos"):
                if arquivo and arquivo.filename:
                    adicionar_anexo_ao_ativo(ativo_id, arquivo, tipo_anexo)

            flash("Ativo atualizado com sucesso.", "success")
            return redirect(url_for("ativos"))
        except Exception as e:
            flash(f"Erro ao atualizar ativo: {e}", "error")
            return redirect(url_for("editar_ativo_web", ativo_id=ativo_id))

    return render_template(
        "ativos/editar.html",
        title="Editar ativo",
        ativo=ativo,
        colaboradores=listar_colaboradores(),
        setores=listar_setores(),
        marcas=listar_marcas(),
        modelos=listar_modelos(),
        tipos=listar_tipos_equipamento(),
        anexos=listar_anexos_do_ativo(ativo_id),
    )


@login_required
def excluir_ativo_web(ativo_id):
    try:
        excluir_ativo(ativo_id)
        flash("Ativo excluído com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao excluir ativo: {e}", "error")
    return redirect(url_for("ativos"))


def registrar_rotas(app):
    app.add_url_rule("/ativos", view_func=ativos, methods=["GET", "POST"])
    app.add_url_rule("/ativos/<int:ativo_id>/editar", view_func=editar_ativo_web, methods=["GET", "POST"])
    app.add_url_rule("/ativos/<int:ativo_id>/excluir", view_func=excluir_ativo_web, methods=["POST"])
