import json
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render,redirect,get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from . models import Author,Article,ArticleForm
# Create your views here.
def index(request):
    
    articles = Article.objects.filter(is_publish=True)
    return render(request, "index.html", {
        'articles': articles
    })
def article(request, id):

    article = get_object_or_404(Article,pk=id)
    is_owner = False
    if article.author.id == request.user.id:
        is_owner=True
    return render (request,"article.html", {
        "article": article,
        "is_owner": is_owner
    })
def dashboard(request):
    articles = request.user.article.all()
    total_article = len(articles)
    total_publish = request.user.article.filter(is_publish = True).count()
    
    return render(request, "dashboard.html",{
        "articles": articles,
        "total_article": total_article,
        "total_publish": total_publish
    })

def handle_publishing(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only route."}, status=400)
    req_data = json.loads(request.body)
    post_id = req_data.get('id', '')
    article = Article.objects.filter(pk = post_id, author = request.user).first()
    if article == None:
        return JsonResponse({"error": "POST not found."},status=400)
    article.is_publish = not article.is_publish
    article.save()
    action_publish = 'Published' if article.is_publish else 'Unpublished'
    msg = 'Article was ' + action_publish
    return JsonResponse({
        "error": "",
        "msg": msg,
        "operation": action_publish
    },status=200)
    return HttpResponse(request)

def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            
            article = form.save(commit=False)
            article.author_id = request.user.id
            article.save()
            messages.success(request,"Post Created")
            return redirect("home")
            
    else:
        form = ArticleForm()
    return render(request, "create_article.html",{
        "form": form
    })
def edit_article(request,id):
    article = get_object_or_404(Article,pk=id)

    if article.author.id != request.user.id:
        return render (request,'error.html')
    else:
        if request.method == "POST":
            form = ArticleForm(request.POST,request.FILES,instance = article)
            if form.is_valid():
                
                article = form.save(commit=False)
                article.author_id = request.user.id
                article.save()
                messages.success(request,"Post Edited")
                return redirect("home")
                
        else:
            form = ArticleForm(instance=article)
        return render(request,'edit_article.html', {
            'form' : form,
            'post_id': article.id
        })

def remove_article(request,id):
    print(id)
    return redirect('dashboard')


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