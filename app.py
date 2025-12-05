from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
    login_required,
)  # Importa LoginManager para gerenciar sessões de usuário

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "your_secret_key"  # chave secreta usada para proteger sessões e formulários
)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///database.db"  # caminho que o sqlalchemy vai usar para criar o banco de dados
)

login_manager = LoginManager()  # instancia do LoginManager
db.init_app(app)  # inicializa a extensão do banco de dados com a aplicação Flask
login_manager.init_app(
    app
)  # inicializa a extensão do LoginManager com a aplicação Flask

# view login
login_manager.login_view = "login"  # define a rota de login


# Session <- Conexão ativa
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # consulta o usuário pelo ID


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Login
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)  # faz o login do usuário
            print(
                current_user.is_authenticated
            )  # verifica se o usuário está autenticado
            return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"}), 400


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})


@app.route("/user", methods=["POST"])
@login_required
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
      user = User(username=username, password=password)
      db.session.add(user)
      db.session.commit()
      return jsonify({"message": "User created successfully"})
      
    return jsonify({"message": "Dados inválidos"}), 401

@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
  user = User.query.get(id_user)
  if user:
    return {"username": user.username}
  return jsonify({"message": "User not found"}), 404

@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
  data = request.get_json()
  user = User.query.get(id_user)
  
  if user and data.get("password"):
    user.password = data.get("password")
    db.session.commit()
    return jsonify({"message": f"User {id_user} updated successfully"})
  return jsonify({"message": f"User {id_user} not found"}), 404

@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
  user = User.query.get(id_user)
  if id_user == current_user.id:
    return jsonify({"message": "You cannot delete your own account"}), 403
  
  if user:
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {id_user} deleted successfully"})
  return jsonify({"message": f"User {id_user} not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
