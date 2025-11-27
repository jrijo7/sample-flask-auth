from database import db
from flask_login import UserMixin # Importa UserMixin para facilitar a integração com Flask-Login
class User(db.Model, UserMixin): # Adiciona UserMixin à classe User
  # id (int), username (text), password (text)
  id = db.Column(db.Integer, primary_key=True) # primary_key=True indica que é a chave primária da tabela
  username = db.Column(db.String(80), nullable=False, unique=True) # nullable=False indica que o campo não pode ser nulo, unique=True indica que o valor deve ser único
  password = db.Column(db.String(80), nullable=False)