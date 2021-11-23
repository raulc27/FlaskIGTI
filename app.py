from flask import Flask, request,jsonify
from data import alchemy
from model import show, episode

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

if __name__ == '__main__':
    from data import alchemy
    alchemy.init_app(app)
    
app.run(port=5000, debug=True)