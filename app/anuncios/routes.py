from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Anuncio, Categoria

bp = Blueprint("anuncios", __name__, url_prefix="/anuncios")


@bp.route("/")
@login_required
def index():
    anuncios = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc()).all()
    return render_template("anuncios/index.html", anuncios=anuncios)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    categorias = Categoria.query.all()
    if request.method == "POST":
        anuncio = Anuncio(titulo=request.form["titulo"],
                          contenido=request.form["contenido"],
                          categoria_id=int(request.form["categoria_id"]),
                          usuario_id=current_user.id)
        db.session.add(anuncio)
        db.session.commit()
        flash("Anuncio publicado", "success")
        return redirect(url_for("anuncios.index"))
    return render_template("anuncios/form.html", anuncio=None, categorias=categorias)


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    anuncio = db.get_or_404(Anuncio, id)
    categorias = Categoria.query.all()
    if request.method == "POST":
        anuncio.titulo = request.form["titulo"]
        anuncio.contenido = request.form["contenido"]
        anuncio.categoria_id = int(request.form["categoria_id"])
        db.session.commit()
        flash("Anuncio actualizado", "success")
        return redirect(url_for("anuncios.index"))
    return render_template("anuncios/form.html", anuncio=anuncio, categorias=categorias)


@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    anuncio = db.get_or_404(Anuncio, id)
    db.session.delete(anuncio)
    db.session.commit()
    flash("Anuncio eliminado", "warning")
    return redirect(url_for("anuncios.index"))