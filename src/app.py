"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({"first_name": "John", "age": 33, "lucky_number": [7,13,22]})
jackson_family.add_member({"first_name": "Jane", "age": 35, "lucky_number": [10,14,3]})
jackson_family.add_member({"first_name": "Jimmy", "age": 5, "lucky_number": [1]})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

#buscamos miembro por ip
@app.route('/member/<int:id>', methods=['GET'])
def get_member_by_id(id):
    member = jackson_family.get_member(id)
    if not member:
       return jsonify({"Msg": "Member not found"}), 404
    return jsonify(member)

#agregamos un miembro
@app.route('/member', methods=['POST'])
def add_members():
    data= request.get_json()
    jackson_family.add_member(data)
    return jsonify({"done": True})

#eliminamos un miembro
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    result= jackson_family.delete_member(id)
    if not result:
        return jsonify({"Msg": "Member not found"}), 404
    return jsonify({"done": True})

#modificamos un miebro
@app.route('/member/<int:id>', methods=['PUT'])
def modify_member(id):
    date= request.get_json()
    result= jackson_family.update_member(id, date)
    if not result:
        return jsonify({"Msg": "Member not updated"}), 404
    return jsonify({"done": True})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
