from pymongo import MongoClient
# local connect
# Local_link = MongoClient("mongodb://localhost:27017/")
Local_link = MongoClient("mongodb+srv://mugi84219:mugesh2002@cluster0.3dld5.mongodb.net/studentMS")
# data base
db = Local_link.studentMS
# collection
admins = db.admins
# students coll
studentcoll = db.students
# cours coll
courscoll = db.course

