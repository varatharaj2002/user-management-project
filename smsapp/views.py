from django.shortcuts import render,redirect
from . import db,services
from bson import ObjectId
import re
# Create your views here.
# login page



def login(req):
    if(req.method == "POST"):
        query = req.POST
        username = query.get("username")
        password = query.get("password")
        user = db.admins.find_one({"username": username, "password": password})
        print(user,"this is user")
        if(not user):
            print("User not found, redirecting to registration.")
            # return render(req,"reg.html",{"message":"user is not exist pls Creat the user!"})
            return redirect("reg")
        else:
            print("triger form-login")
            id = str(user['_id'])
            print(id,user['username'])
            print("session is ",req.session)
            req.session['userId'] = id
            return redirect("home")
    return render(req, "login.html")

# register page
def reg(req):
    if(req.method == "POST"):
        print("reg block")
        query = req.POST
        username = query.get("username")
        password = query.get("password")
        confirmpassword = query.get("confirmpassword")
        
        username_pattern = re.compile(r"^(?=.*[a-zA-Z])[a-zA-Z0-9_]{5,15}$")
        password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
        
        if(not username_pattern.match(username)):
            return render(req,"reg.html",{"usernameerror":"letters, digits, and underscores length to between 5 and 15 characters!"})
        if(not password_pattern.match(password)):
            return render(req,"reg.html",{"passwordError":"Requires at least one lowercase letter, one uppercase letter, and one digit. minimum length of 8 character!"})
        
        if(confirmpassword == password):
           
            exists = db.admins.find_one({"username": username})
            if(exists):
                print("exists",exists)
                return render(req, "reg.html", {"message": "This username already exists. Try another name!"})
            else:
                print("else part")
                db.admins.insert_one({"username": username, "password": password})
                return redirect("login")
        else:
            return render(req, "reg.html", {"message": "This confirm password and password is mismatch !"})
    return render(req, "reg.html")
# home page
def home(req):
    print("trigger")
    sessionId = req.session.get("userId") 
    print(sessionId,"session_user")
    if not sessionId:
        return redirect("login")
    user = services.findUser(sessionId)
    print("user is ",user)
    students = db.studentcoll.find({"adminId":user["_id"]}).limit(3)
    courses = db.courscoll.find({"adminId":user["_id"]}).limit(3)
    context = {
        "students": students,
        "courses": courses,
        "user": user  
    }

    return render(req, "home.html", context)
# add student
def addstudent(req):
    users = db.admins.find()
    sessionId = req.session.get("userId")
    user = services.findUser(sessionId)
    if(not sessionId):
        return redirect("login")
    if(req.method == "POST"):
        print("reg block")
        query = req.POST
        username = query.get("username")
        email = query.get("email")
        birthday = query.get("birthday")
        age = query.get("age")
        phoneNumber = query.get("phoneNumber")
        gender = query.get("gender")
        degree = query.get("degree")
        course = query.get("course")
        db.studentcoll.insert_one({"username":username,"email":email,"birthday":birthday,
                            "age":age,"phoneNumber":phoneNumber,"gender":gender,
                            "degree":degree,"course":course,"adminId":user["_id"]})
        print("redirect block")
        return redirect("students")
    return render(req,"addStudent.html",{"users":users,"user":user})
# students
def students(req):
    sessionId = req.session.get("userId")
    user = services.findUser(sessionId)
    if not sessionId:
        return redirect("login") 
    print("working")
    students = db.studentcoll.find({"adminId":user["_id"]})
    datas = []
    for i in students:
        i["docId"] = str(i["_id"])
        datas.append(i)
    return render(req, "students.html", {"students": datas,"user":user})

# logout
def logout(req):
    del req.session["userId"]
    print(req.session.keys())
    return redirect("login")
# about
def about(req):
    users = db.admins.find()
    sessionId = req.session.get("userId")
    user = services.findUser(sessionId)
    print("about",user)
    if(not sessionId):
        return redirect("login")
    return render(req,"about.html",{"users":users,"user":user})
# cours
def course(req):
    sessionId = req.session.get("userId")
    user = services.findUser(sessionId)
    if not sessionId:
        return redirect("login") 
    print("working")
    courses = db.courscoll.find({"adminId":user["_id"]})
    data = []
    for i in courses:
        i["docId"] = str(i["_id"])
        data.append(i)
    return render(req, "course.html", {"courses": data,"user":user})  

# addCours
def addcourse(req):
    users = db.admins.find()
    sessionId = req.session.get("userId")
    user = services.findUser(sessionId)
    if(not sessionId):
        return redirect("login")
    if(req.method == "POST"):
        print("reg block")
        query = req.POST
        coursename = query.get("coursename")
        duration = query.get("duration")
        Specialties = query.get("Specialties")
        description = query.get("description")
        db.courscoll.insert_one({"coursename":coursename,"duration":duration,"Specialties":Specialties,"description":description,"adminId":user["_id"]})
        print("redirect block")
        return redirect("course")
    return render(req,"addcourse.html",{"users":users,"user":user})

# delet student
def deleteStudent(req, id):
    print(req.method, "this is method")
    if req.method == "GET":
        print("delete student", id)
        object_id = ObjectId(id)
        db.studentcoll.delete_one({"_id": object_id})
    return redirect("students")
# deleteCours
def deletecourse(req,id):
    print("delete course",req.method)
    if (req.method == "GET"):
        print(req.method,"req method cours")
        print("delete cours", id)
        objectId = ObjectId(id)
        db.courscoll.delete_one({"_id": objectId})
        return redirect("course")
#edit course
def editcourse(req,id):
    courseId = ObjectId(id)
    sessionId = req.session.get("userId")
    user = services.findUser(sessionId)
    course = db.courscoll.find_one({"_id":courseId})
    if(not sessionId):
        return redirect("login")
    if(req.method == "POST"):
        print("reg block")
        query = req.POST
        coursename = query.get("coursename")
        duration = query.get("duration")
        Specialties = query.get("Specialties")
        description = query.get("description")
        db.courscoll.find_one_and_update({"_id":courseId},{"$set":{"coursename":coursename,"duration":duration,"Specialties":Specialties,"description":description,}})
        print("redirect block")
        return redirect("course")
    return render(req,"editcourse.html",{"course":course,"user":user})
# edit student
def editStudents(req,id):
    studentId = ObjectId(id)
    sessionId = req.session.get("userId")
    user = services.findUser(sessionId)
    student = db.studentcoll.find_one({"_id":studentId})
    if(not sessionId):
        return redirect("login")
    if(req.method == "POST"):
        query = req.POST
        username = query.get("username")
        email = query.get("email")
        birthday = query.get("birthday")
        age = query.get("age")
        phoneNumber = query.get("phoneNumber")
        gender = query.get("gender")
        degree = query.get("degree")
        course = query.get("course")
        db.studentcoll.find_one_and_update({"_id":studentId},{"$set":{"username":username,"email":email,"birthday":birthday,"age":age,"phoneNumber":phoneNumber,"gender":gender,"degree":degree,"course":course,}})
        print("redirect block")
        return redirect("students")
    return render(req,"editStudents.html",{"student":student,"user":user})
