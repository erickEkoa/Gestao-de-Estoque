import csv
import io
from flask import request, send_file
from gestao_ativos.auth import login_required
from gestao_ativos.repositorios.ativos import buscar_ativos


@login_required
def exportar_csv():
    dados = buscar_ativos(
        request.args.get("numero_serie", "").strip(),
        request.args.get("modelo", "").strip(),
        request.args.get("colaborador", "").strip(),
        request.args.get("tipo", "").strip(),
    )

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow([
        "ID", "Data Cadastro", "Número de Série", "Descrição", "Colaborador",
        "Setor", "Marca", "Modelo", "Tipo de Equipamento", "Status", "Observação", "Total de Anexos"
    ])

    for item in dados:
        writer.writerow([
            item["id"], item["data_cadastro"], item["numero_serie"], item["descricao"],
            item["colaborador"], item["setor"], item["marca"], item["modelo"],
            item["tipo_equipamento"], item["status"], item["observacao"], item["total_anexos"]
        ])

    mem = io.BytesIO()
    mem.write(output.getvalue().encode("utf-8-sig"))
    mem.seek(0)
    output.close()
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="ativos.csv")


def registrar_rotas(app):
    app.add_url_rule("/exportar-csv", view_func=exportar_csv)
