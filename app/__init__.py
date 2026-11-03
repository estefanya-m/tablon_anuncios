from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from . import models  # para que Migrate vea las tablas

    from .main.routes import bp as main_bp
    from .auth.routes import bp as auth_bp
    from .usuarios.routes import bp as usuarios_bp
    from .categorias.routes import bp as categorias_bp
    from .anuncios.routes import bp as anuncios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(anuncios_bp)

    return app