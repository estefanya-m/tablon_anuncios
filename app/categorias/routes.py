from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..extensions import db
from ..models import Categoria

bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@bp.route("/")
@login_required
def index():
    categorias = Categoria.query.all()
    return render_template("categorias/index.html", categorias=categorias)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        categoria = Categoria(nombre=request.form["nombre"],
                              descripcion=request.form["descripcion"])
        db.session.add(categoria)
        db.session.commit()
        flash("Categoría registrada", "success")
        return redirect(url_for("categorias.index"))
    return render_template("categorias/form.html", categoria=None)


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    categoria = db.get_or_404(Categoria, id)
    if request.method == "POST":
        categoria.nombre = request.form["nombre"]
        categoria.descripcion = request.form["descripcion"]
        db.session.commit()
        flash("Categoría actualizada", "success")
        return redirect(url_for("categorias.index"))
    return render_template("categorias/form.html", categoria=categoria)


@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    categoria = db.get_or_404(Categoria, id)
    db.session.delete(categoria)
    db.session.commit()
    flash("Categoría eliminada", "warning")
    return redirect(url_for("categorias.index"))