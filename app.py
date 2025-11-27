from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager # Importa LoginManager para gerenciar sessões de usuário

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" # chave secreta usada para proteger sessões e formulários
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db" #caminho que o sqlalchemy vai usar para criar o banco de dados

login_manager = LoginManager() # instancia do LoginManager
db.init_app(app) # inicializa a extensão do banco de dados com a aplicação Flask
login_manarger.init_app(app) # inicializa a extensão do LoginManager com a aplicação Flask

# view login

@app.route('/login', methods = ['POST'])
def login():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')
  
  if username and password:
    # Login
    pass
  
  return jsonify({'message': 'Invalid credentials'}), 400

@app.route('/hello-world', methods=['GET'])
def hello_world():
    return 'Hello, World!'
  
if __name__ == '__main__':
  app.run(debug=True)