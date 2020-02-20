"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for, make_response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Budget, Children
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/profilecreation', methods=['POST'])
@app.route('/profilecreation/<user_email>', methods=["GET"])
def handle_profilecreation(user_email=""):

    response_body = {
        "hello": "world"
    }
    # requesting_user = User.query.filter_by(id=username).all()
    posting_user_email = request.json["email"]
    if request.method == "GET":
        requesting_user = User.query.filter_by(email=user_email).one_or_none()
    else:
        requesting_user = User.query.filter_by(email=posting_user_email).one_or_none()
    
    print(requesting_user)
    if request.method == "GET":
        
        if user_email:
            
            if requesting_user:
                # user exists
                status_code = 200
                response_body = {
                    "result": "El usuario esta registrado"
                }
            else:
                # user does not exist
                status_code = 404
                response_body = {
                    "result": "El usuario no existe"
                }
        else:
            # bad request no user email on url
            status_code = 400
            response_body = {
                "result": "No hay user email en la url"
            }

    elif request.method == "POST":
        new_user_data = request.json
        if requesting_user:
            # actualizo los datos porque existe
            requesting_user.update(new_user_data)
            owner_user_id = requesting_user.id
            Budget.query.filter_by(user_userid=requesting_user.id).delete()
            Children.query.filter_by(user_userid=requesting_user.id).delete()

        else:
            # creo al nuevo usuario
            print("trying to create")
            new_user = User(new_user_data)
            db.session.add(new_user)
            
            db.session.commit()
            owner_user_id = new_user.id
        
        # try:
            
        status_code = 201
        print("first commit success")
        
        # create budgets
        budget = Budget(new_user_data["thebudget"], owner_user_id)
        db.session.add(budget)
        children_data = new_user_data["thechildren"]
        for child in new_user_data["thechildren"]:
            new_child = Children(child, owner_user_id)
            db.session.add(new_child)
        

        result = "Ya estás anotado para la próxima entrega de The Box Regardée" 
        response_body = {
            "result": result
        }
        # except:
        #    print('explote')
        #    status_code = 400
        #    response_body = {
        #        "result": "La info no fue almacenada"
        #    }
        db.session.commit()
    return make_response(
    jsonify(response_body),
    status_code)


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
