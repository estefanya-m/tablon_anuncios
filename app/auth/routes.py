from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import Usuario

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(password):
            login_user(usuario)
            return redirect(url_for("main.index"))
        flash("Correo o contraseña incorrectos", "danger")
    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))