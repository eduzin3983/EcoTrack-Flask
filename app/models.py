from datetime import datetime, timezone
from flask_login import UserMixin
from app import db

class Usuarios(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class RegistrosDiarios(db.Model):
    __tablename__ = 'registros_diarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_registro = db.Column(db.Date, nullable=False)
    agua = db.Column(db.Float, nullable=False)
    energia = db.Column(db.Float, nullable=False)
    residuos = db.Column(db.Float, nullable=False)
    transporte = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Sugestoes(db.Model):
    __tablename__ = 'sugestoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topico = db.Column(db.String(50), nullable=False)
    impacto = db.Column(db.String(50), nullable=False)
    texto_sugestao = db.Column(db.Text, nullable=False)
