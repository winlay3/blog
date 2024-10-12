from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render,redirect
from django.db import IntegrityError
from . models import Author,Article
# Create your views here.
def index(request):
    articles = Article.objects.all()
    return render(request, "index.html", {
        'articles': articles
    })

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if username == '' or email == '' or password== '':
            return render(request, "signup.html",{
                "message" : "Username, email and password fields cannot be blank!"
            })
        email_already_exit =Author.objects.filter(email= email).first()
        if email_already_exit != None:
            return render(request, "signup.html",{
                "message" : "email already exit"
            })

        try:
            user = Author.objects.create_user(username,email,password)
            user.save()
        except IntegrityError as e:
            return render(request, "signup.html",{
                "message" : "Username already exit!"
            })
        return redirect("login")
    return render(request,"signup.html")
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("home")
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username= username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "message": "Username or password is invalid"
            })
    return render(request,"login.html")