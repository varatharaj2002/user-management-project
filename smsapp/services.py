from . import db
from bson import ObjectId


def findUser(userId):
    userObjId = ObjectId(userId)
    user = db.admins.find_one({"_id":userObjId})
    return user

def getUserId(userId):
    return ObjectId(userId)