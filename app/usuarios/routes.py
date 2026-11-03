from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Usuario

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.route("/")
@login_required
def index():
    usuarios = Usuario.query.all()
    return render_template("usuarios/index.html", usuarios=usuarios)


@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        email = request.form["email"]
        if Usuario.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado", "danger")
            return render_template("usuarios/form.html", usuario=None)
        usuario = Usuario(nombre=request.form["nombre"], email=email)
        usuario.set_password(request.form["password"])
        db.session.add(usuario)
        db.session.commit()
        flash("Usuario registrado correctamente", "success")
        if current_user.is_authenticated:
            return redirect(url_for("usuarios.index"))
        return redirect(url_for("auth.login"))
    return render_template("usuarios/form.html", usuario=None)


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    usuario = db.get_or_404(Usuario, id)
    if request.method == "POST":
        usuario.nombre = request.form["nombre"]
        usuario.email = request.form["email"]
        if request.form["password"]:
            usuario.set_password(request.form["password"])
        db.session.commit()
        flash("Usuario actualizado", "success")
        return redirect(url_for("usuarios.index"))
    return render_template("usuarios/form.html", usuario=usuario)


@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    usuario = db.get_or_404(Usuario, id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado", "warning")
    return redirect(url_for("usuarios.index"))