"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "other": 'another thing'
    }

    return jsonify(response_body), 200

@app.route('/person', methods=['GET'])
def handle_person(): 
    return jsonify('Hola mundo'), 200


@app.route('/students', methods=['GET', 'POST'])
def handle_students(): 
    if request.method == 'POST': 
       ## Insert en la base de datos 

        return jsonify('Ha recibido un post'), 200
    elif request.method == 'GET':

        ## obtener la información y retornarla
        return jsonify('Ha recibido un GET'), 200
    
    return jsonify('error'), 400

@app.route('/students/<int:id>', methods=['DELETE'])
def handle_delete_students(id): 
    ## eliminar el estudiante 
    ## [1,2,3,4]
    if id == 4:
        return jsonify({}), 204
    else: 
        return jsonify({ 'msg': 'estudiante no encontrado'}), 404
    
@app.route('/students/<int:id>', methods=['PUT'])
def handle_update_students(id): 
    ## eliminar el estudiante 
    ## [1,2,3,4]
    if id == 4:
        return jsonify({}), 204
    else: 
        return jsonify({ 'msg': 'estudiante no encontrado'}), 404
    
@app.route('/students/<int:id>', methods=['GET'])
def handle_get_students(id): 
    ## eliminar el estudiante 
    ## [1,2,3,4]
    if id == 4:
        return jsonify({}), 204
    else: 
        return jsonify({ 'msg': 'estudiante no encontrado'}), 404
    

@app.route('/person', methods=['POST'])
def create_person():
    # POST request
    body = request.get_json()  # Obtener el request body de la solicitud
    print(body)
    if body is None:
        return "El cuerpo de la solicitud es null", 400
    if 'first_name' not in body:
        return 'Debes especificar first_name', 400
    if 'last_name' not in body:
        return 'Debes especificar last_name', 400
    
    ## Crear usuario en la base de datos!! 

    return "ok", 200

        
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
