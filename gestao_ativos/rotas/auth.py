from flask import flash, redirect, render_template, request, session, url_for
from gestao_ativos.repositorios.usuarios import validar_login


def index():
    if "usuario" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


def login():
    if request.method == "POST":
        login_usuario = request.form.get("login", "").strip()
        senha = request.form.get("senha", "").strip()

        if not login_usuario or not senha:
            flash("Informe usuário e senha.", "warning")
            return redirect(url_for("login"))

        try:
            usuario = validar_login(login_usuario, senha)
            if usuario:
                session["usuario"] = {
                    "id": usuario["id"],
                    "nome": usuario["nome"],
                    "login": usuario["login"]
                }
                flash("Login realizado com sucesso.", "success")
                return redirect(url_for("dashboard"))
            flash("Usuário ou senha inválidos.", "error")
        except Exception as e:
            flash(f"Falha ao autenticar: {e}", "error")
        return redirect(url_for("login"))

    return render_template("auth/login.html", title="Login")


def logout():
    session.clear()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("login"))


def registrar_rotas(app):
    app.add_url_rule("/", view_func=index, methods=["GET"])
    app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=logout)
