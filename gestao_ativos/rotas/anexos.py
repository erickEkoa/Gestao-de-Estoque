import io
from flask import flash, redirect, send_file, url_for
from gestao_ativos.auth import login_required
from gestao_ativos.repositorios.anexos import buscar_anexo_por_id, excluir_anexo


@login_required
def baixar_anexo_ativo(anexo_id):
    anexo = buscar_anexo_por_id(anexo_id)
    if not anexo:
        flash("Anexo não encontrado.", "error")
        return redirect(url_for("ativos"))

    mem = io.BytesIO(bytes(anexo["arquivo"]))
    mem.seek(0)
    return send_file(
        mem,
        mimetype=anexo["tipo_arquivo"] or "application/octet-stream",
        as_attachment=True,
        download_name=anexo["nome_original"]
    )


@login_required
def excluir_anexo_ativo_web(anexo_id):
    anexo = buscar_anexo_por_id(anexo_id)
    if not anexo:
        flash("Anexo não encontrado.", "error")
        return redirect(url_for("ativos"))

    ativo_id = anexo["ativo_id"]
    try:
        excluir_anexo(anexo_id)
        flash("Anexo excluído com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao excluir anexo: {e}", "error")
    return redirect(url_for("editar_ativo_web", ativo_id=ativo_id))


def registrar_rotas(app):
    app.add_url_rule("/anexos/<int:anexo_id>/baixar", view_func=baixar_anexo_ativo)
    app.add_url_rule("/anexos/<int:anexo_id>/excluir", view_func=excluir_anexo_ativo_web, methods=["POST"])
