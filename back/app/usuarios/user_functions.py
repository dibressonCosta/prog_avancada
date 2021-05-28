# from app import app
from app import db
# from bson.objectid import ObjectId
from unidecode import unidecode
import logging
from bson.objectid import ObjectId
logging.basicConfig(level=logging.INFO)

def getCODE():
    from datetime import datetime
    dataHora = datetime.now()
    code = str(dataHora.year)
    code += str(dataHora.month)
    code += str(dataHora.day)
    code += str(dataHora.hour)
    code += str(dataHora.minute)
    code += str(dataHora.second)
    code = str(int(round(int(code)/2, 0)))
    return code

def salvarNovo(email, senha):
    try:
        email = email
        senha = senha
        code = getCODE()
        db.usuario.insert_one(
            {"email": email,
             "senha": senha,
             "code": code})
        return True
    except:
        return False


def entrar(email, senha):
    email = email.strip()
    senha = senha.strip()
    code = getCODE()
    usuario = db.usuario.find(
        {"email": email, "senha": senha})
    if usuario.count() > 0:
        db.usuario.update_one({'email': email}, {"$set": {'code': code}})
        usuario = db.usuario.find(
        {"email": email, "senha": senha})
        return usuario
    else:
        return False


def validate(email, id,code):
    email = email.strip()
    id = id.strip()
    usuario = db.usuario.find(
         {"email": email, "_id": ObjectId(id), "code":code})
    if usuario.count() > 0:
        return usuario
    else:
        return False
