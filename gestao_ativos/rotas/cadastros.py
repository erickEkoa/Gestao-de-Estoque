from flask import flash, redirect, render_template, request, url_for
from gestao_ativos.auth import login_required
from gestao_ativos.repositorios.cadastros import (
    atualizar_colaborador,
    atualizar_marca,
    atualizar_modelo,
    atualizar_setor,
    atualizar_tipo_equipamento,
    buscar_colaborador_por_id,
    buscar_marca_por_id,
    buscar_modelo_por_id,
    buscar_setor_por_id,
    buscar_tipo_por_id,
    excluir_colaborador,
    excluir_marca,
    excluir_modelo,
    excluir_setor,
    excluir_tipo_equipamento,
    inserir_colaborador,
    inserir_marca,
    inserir_modelo,
    inserir_setor,
    inserir_tipo_equipamento,
    listar_colaboradores,
    listar_marcas,
    listar_modelos,
    listar_setores,
    listar_tipos_equipamento,
)


@login_required
def cadastros():
    tipo_form = request.form.get("tipo_form")
    try:
        if request.method == "POST":
            if tipo_form == "setor":
                inserir_setor(request.form.get("nome", "").strip())
                flash("Setor cadastrado com sucesso.", "success")
            elif tipo_form == "colaborador":
                inserir_colaborador(request.form.get("nome", "").strip(), request.form.get("email", "").strip() or None)
                flash("Colaborador cadastrado com sucesso.", "success")
            elif tipo_form == "marca":
                inserir_marca(request.form.get("nome", "").strip())
                flash("Marca cadastrada com sucesso.", "success")
            elif tipo_form == "modelo":
                inserir_modelo(request.form.get("nome", "").strip())
                flash("Modelo cadastrado com sucesso.", "success")
            elif tipo_form == "tipo":
                inserir_tipo_equipamento(request.form.get("nome", "").strip())
                flash("Tipo de equipamento cadastrado com sucesso.", "success")
            return redirect(url_for("cadastros"))
    except Exception as e:
        flash(f"Erro ao salvar cadastro auxiliar: {e}", "error")
        return redirect(url_for("cadastros"))

    return render_template(
        "cadastros/index.html",
        title="Cadastros auxiliares",
        setores=listar_setores(),
        colaboradores=listar_colaboradores(),
        marcas=listar_marcas(),
        modelos=listar_modelos(),
        tipos=listar_tipos_equipamento(),
    )


@login_required
def excluir_setor_web(item_id):
    try:
        excluir_setor(item_id)
        flash("Setor excluído com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao excluir setor: {e}", "error")
    return redirect(url_for("cadastros"))


@login_required
def excluir_colaborador_web(item_id):
    try:
        excluir_colaborador(item_id)
        flash("Colaborador excluído com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao excluir colaborador: {e}", "error")
    return redirect(url_for("cadastros"))


@login_required
def excluir_marca_web(item_id):
    try:
        excluir_marca(item_id)
        flash("Marca excluída com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao excluir marca: {e}", "error")
    return redirect(url_for("cadastros"))


@login_required
def excluir_modelo_web(item_id):
    try:
        excluir_modelo(item_id)
        flash("Modelo excluído com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao excluir modelo: {e}", "error")
    return redirect(url_for("cadastros"))


@login_required
def excluir_tipo_web(item_id):
    try:
        excluir_tipo_equipamento(item_id)
        flash("Tipo excluído com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao excluir tipo: {e}", "error")
    return redirect(url_for("cadastros"))


@login_required
def editar_setor_web(item_id):
    setor = buscar_setor_por_id(item_id)
    if not setor:
        flash("Setor não encontrado.", "error")
        return redirect(url_for("cadastros"))

    if request.method == "POST":
        try:
            atualizar_setor(item_id, request.form.get("nome", "").strip())
            flash("Setor atualizado com sucesso.", "success")
            return redirect(url_for("cadastros"))
        except Exception as e:
            flash(f"Erro ao atualizar setor: {e}", "error")
            return redirect(url_for("editar_setor_web", item_id=item_id))

    return render_template("cadastros/editar_setor.html", title="Editar setor", item=setor)


@login_required
def editar_colaborador_web(item_id):
    colaborador = buscar_colaborador_por_id(item_id)
    if not colaborador:
        flash("Colaborador não encontrado.", "error")
        return redirect(url_for("cadastros"))

    if request.method == "POST":
        try:
            atualizar_colaborador(
                item_id,
                request.form.get("nome", "").strip(),
                request.form.get("email", "").strip() or None
            )
            flash("Colaborador atualizado com sucesso.", "success")
            return redirect(url_for("cadastros"))
        except Exception as e:
            flash(f"Erro ao atualizar colaborador: {e}", "error")
            return redirect(url_for("editar_colaborador_web", item_id=item_id))

    return render_template(
        "cadastros/editar_colaborador.html",
        title="Editar colaborador",
        item=colaborador,
    )


@login_required
def editar_marca_web(item_id):
    marca = buscar_marca_por_id(item_id)
    if not marca:
        flash("Marca não encontrada.", "error")
        return redirect(url_for("cadastros"))

    if request.method == "POST":
        try:
            atualizar_marca(item_id, request.form.get("nome", "").strip())
            flash("Marca atualizada com sucesso.", "success")
            return redirect(url_for("cadastros"))
        except Exception as e:
            flash(f"Erro ao atualizar marca: {e}", "error")
            return redirect(url_for("editar_marca_web", item_id=item_id))

    return render_template("cadastros/editar_marca.html", title="Editar marca", item=marca)


@login_required
def editar_modelo_web(item_id):
    modelo = buscar_modelo_por_id(item_id)
    if not modelo:
        flash("Modelo não encontrado.", "error")
        return redirect(url_for("cadastros"))

    if request.method == "POST":
        try:
            atualizar_modelo(item_id, request.form.get("nome", "").strip())
            flash("Modelo atualizado com sucesso.", "success")
            return redirect(url_for("cadastros"))
        except Exception as e:
            flash(f"Erro ao atualizar modelo: {e}", "error")
            return redirect(url_for("editar_modelo_web", item_id=item_id))

    return render_template("cadastros/editar_modelo.html", title="Editar modelo", item=modelo)


@login_required
def editar_tipo_web(item_id):
    tipo = buscar_tipo_por_id(item_id)
    if not tipo:
        flash("Tipo de equipamento não encontrado.", "error")
        return redirect(url_for("cadastros"))

    if request.method == "POST":
        try:
            atualizar_tipo_equipamento(item_id, request.form.get("nome", "").strip())
            flash("Tipo de equipamento atualizado com sucesso.", "success")
            return redirect(url_for("cadastros"))
        except Exception as e:
            flash(f"Erro ao atualizar tipo de equipamento: {e}", "error")
            return redirect(url_for("editar_tipo_web", item_id=item_id))

    return render_template(
        "cadastros/editar_tipo.html",
        title="Editar tipo de equipamento",
        item=tipo,
    )


def registrar_rotas(app):
    app.add_url_rule("/cadastros", view_func=cadastros, methods=["GET", "POST"])
    app.add_url_rule("/cadastros/setores/<int:item_id>/excluir", view_func=excluir_setor_web, methods=["POST"])
    app.add_url_rule("/cadastros/colaboradores/<int:item_id>/excluir", view_func=excluir_colaborador_web, methods=["POST"])
    app.add_url_rule("/cadastros/marcas/<int:item_id>/excluir", view_func=excluir_marca_web, methods=["POST"])
    app.add_url_rule("/cadastros/modelos/<int:item_id>/excluir", view_func=excluir_modelo_web, methods=["POST"])
    app.add_url_rule("/cadastros/tipos/<int:item_id>/excluir", view_func=excluir_tipo_web, methods=["POST"])
    app.add_url_rule("/cadastros/setores/<int:item_id>/editar", view_func=editar_setor_web, methods=["GET", "POST"])
    app.add_url_rule("/cadastros/colaboradores/<int:item_id>/editar", view_func=editar_colaborador_web, methods=["GET", "POST"])
    app.add_url_rule("/cadastros/marcas/<int:item_id>/editar", view_func=editar_marca_web, methods=["GET", "POST"])
    app.add_url_rule("/cadastros/modelos/<int:item_id>/editar", view_func=editar_modelo_web, methods=["GET", "POST"])
    app.add_url_rule("/cadastros/tipos/<int:item_id>/editar", view_func=editar_tipo_web, methods=["GET", "POST"])
