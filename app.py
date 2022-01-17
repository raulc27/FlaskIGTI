from flask import Flask, request,jsonify
from data import alchemy
from model import show, episode

#Autenticacao e Autorização com JWT
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from datetime import timedelta

from model import user
from werkzeug.security import generate_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JSON_SORT_KEYS'] = False

app.config['JWT_SECRET_KEY'] = 'XItVYn2Hlgdq4TsoR5Lpicgw15I'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)

jwt = JWTManager(app)

app.secret_key = 'supersecreto'


@app.route('/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    new_user = user.UserModel(username, generate_password_hash(password))
    try:
        new_user.save_to_db()
        return new_user.json()
    except:
        return {'message':'Usuário já existe!'}, 409


@app.route('/user/<string:username>')
def get_user(username):
    result = user.UserModel.find_by_username(username)
    if result:
        return result.json()
    return {'message':'Usuário não encontrado'}, 404

@app.route('/user/<string:username>', methods=['DELETE'])
def delete_user(username):
    result = user.UserModel.find_by_username(username)
    if result:
        result.delete_from_db()
        return {'message':'Usuário excluído com sucesso!'}, 202
    else:
        return {'message':'Usuário não encontrado!'}, 404


# rota para auth
@app.route("/login",methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    result = user.UserModel.find_by_username(username)
    if result and check_password_hash(result.passowrd, password):
        access_token = create_access_token(identity=username, fresh=True)
        return {'token de acesso':'access_token'}
    else:
        return {'message':'Usuário ou senha inválido!'}, 401

# retorna identidade de usuario de um token
@app.route("/autenticado")
@jwt_required()
def logado():
    current_user = get_jwt_identity()
    return {'usuário do token':current_user}, 200


@app.before_first_request
def create_tables():
    alchemy.create_all()

@app.route('/', methods=['GET'])
def home():
    return "API funcionando...", 200

@app.route('/show',methods=['POST'])
def create_show():
    request_data = request.get_json()
    new_show = show.ShowModel(request_data['name'])
    new_show.save_to_db()
    print(new_show.id)
    result = show.ShowModel.find_by_id(new_show.id)
    return jsonify(result.json())

@app.route('/show/<string:name>')
def get_show(name):
    result = show.ShowModel.find_by_name(name)
    if result:
        return result.json()
    return {'message':'Série não encontrada'}, 404

@app.route('/show/<string:name>/episode',methods=['POST'])
def create_episode_in_show(name):
    request_data = request.get_json()
    parent = show.ShowModule.find_by_name(name)
    if parent:
        new_episode = episode.EpisodeModel(name=request_data['name'], season=request_data['season'],show_id=parent.id)
        new_episode.save_to_db()
        return new_episode.json()
    else:
        return {'nessage':'Série não encontrada'}, 404

@app.route('/show/<int:id>', methods=['DELETE'])
def delete_show(id):
    result = show.ShowModel.find_by_id(id)
    if result:
        result.delete_from_db();
        return {'message':'Excluido com sucesso'}, 202
    else:
        return {'message':'Série não encontrada!!'}, 404

@app.route('/show/<int:id>', methods=['DELETE'])
def delete_episode(id):
    result = episode.EpisodeModel.find_by_id(id)
    if result:
        result.delete_from_db()
        return {'message':'Excluído com scuesso!'}, 202
    else:
        return {'message':'Episódio não encontrado'}, 404

@app.route('/shows')
@jwt_required()
def list():
    result = show.ShowModel.list_shows()
    return {'showlist':result},200

@app.route('/show/<int:int>/update', methods=['PUT'])
def update_show(id):
    request_data = request.get_json()
    result = show.ShowModel.find_by_id(id)
    if result:
        result.name = request_data['name']
        result.update()
        return {'message':'Série atualizada com sucesso'}, 200
    else:
        return {'message':'Série não encontrada'}, 404

if __name__ == '__main__':
    from data import alchemy
    alchemy.init_app(app)
    app.run(port=5000, debug=True)