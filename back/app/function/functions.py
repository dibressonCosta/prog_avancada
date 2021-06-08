from app import db
from bson.objectid import ObjectId



def salvarNovo(name,details, start, end, color, userId):
    try:
        db.agenda.insert_one(
            {"name": name,
             "details": details,
             "start": start,
             "end": end,
             "color": color,
             "userId": userId,
             }
        )
        return True
    except:
        return False


def salvarEdicao(id,name,details, start, end, color):
    if id is not None and db.agenda.find_one({'_id': ObjectId(id)}) is not None:
        try:
            result = db.agenda.update_one({'_id': ObjectId(id)}, {"$set": {'name': name, 'details': details,
                             'start': start, 'end': end, 'color': color}})
            return True
        except:
            return False
    else:
        return False
def salvarDelecao(id):
    try:
        result = db.agenda.delete_one({'_id': ObjectId(id)})
        if(result.deleted_count > 0):
            return True
        else:
            return False
    except:
        return False
