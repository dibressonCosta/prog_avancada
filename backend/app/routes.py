from flask import json, request, jsonify
import flask
from bson import json_util
from app import app
from app import db
from bson.objectid import ObjectId

@app.route('/')
@app.route('/index')

def index():
    return flask.jsonify(json.loads(json_util.dumps(db.agenda.find({}).sort("_id", 1))))

@app.route('/create', methods=['POST'])
def create():
    json_data = request.form.to_dict()
    if json_data is not None:
        db.agenda.insert_one(json_data)
        return jsonify(mensagem='agenda criado')
    else:
        return jsonify(mensagem='agenda não criado')

@app.route("/getid/<string:userId>")
def getid(userId):
    agenda = db.agenda.find_one({"_id": ObjectId(userId)})
    return flask.jsonify(json.loads(json_util.dumps(agenda)))

@app.route("/delete/<string:userId>")
def delete(userId):
    result = db.agenda.delete_one({"_id": ObjectId(userId)})
    if(result.deleted_count > 0):
        return jsonify(mensagem='agenda removido')
    else:
        return jsonify(mensagem='agenda não removido')

@app.route('/update', methods=['POST'])
def update():
    json_data = request.form.to_dict()
    if json_data is not None and db.agenda.find_one({"_id": ObjectId(json_data["id"])}) is not None:
        db.agenda.update_one({'_id': ObjectId(json_data["id"])}, {"$set": {'nome':
        json_data["nome"], 'email': json_data["email"]}})
        return jsonify(mensagem='agenda atualizado')
    else:
        return jsonify(mensagem='agenda não atualizado')
