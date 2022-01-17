from flask import Flask, request,jsonify
from data import alchemy
from model import show

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True

app.secret_key = 'supersecreto'

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
    show_deleted = show.ShowModel.find_by_name(id)
    show_deleted.delete_from_db();
    return {'message':'Excluido com sucesso'}, 202

@app.route('/show/<int:id>', methods=['DELETE'])
def delete_episode(id):
    show_deleted = episode.EpisodeModel.find_by_id(id)
    show_deleted.delete_from_db()
    return {'message':'Excluído com scuesso!'}, 202

@app.route('/shows')
def list():
    result = show.ShowModel.list_shows()
    return {'showlist':result},200

if __name__ == '__main__':
    from data import alchemy
    alchemy.init_app(app)
    
app.run(port=5000, debug=True)