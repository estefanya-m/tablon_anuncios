class Config:
    SECRET_KEY = "clave-secreta-tablon-2026"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:admin@localhost:5432/bd_anuncios"
    SQLALCHEMY_TRACK_MODIFICATIONS = False