from django.urls import path
from . import views

urlpatterns = [
    path("",views.login,name="login"),
    path("reg/",views.reg,name="reg"),
    path("home/",views.home,name="home"),
    path("addstudent/",views.addstudent,name="addstudent"),
    path("students/",views.students,name="students"),
    path("logout/", views.logout, name="logout"),
    path("about/", views.about, name="about"),
    path("course/", views.course, name="course"),
    path("addcourse/", views.addcourse, name="addcourse"),
    path("delete/<str:id>",views.deleteStudent,name="deleteStudent"),
    path("course/delete/<str:id>",views.deletecourse,name="deletecourse"),
    path("editcourse/<str:id>", views.editcourse, name="editcourse"),
    path("editStudents/<str:id>",views.editStudents,name="editStudents"),
    
]
