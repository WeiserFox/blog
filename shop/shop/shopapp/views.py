from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from . import models
from django.contrib.auth import login, authenticate, logout
import datetime
from django.core.files.storage import FileSystemStorage
from . import email_code
import random
from asgiref.sync import sync_to_async
import re

AUTH_REQUIRED_MSG = "Войдите в учётную запись"


class Home(View):
    def get(self, request):
        posts = models.Post.objects.all()
        return render(request, "index.html", {"articles": posts})


class Post(View):
    def get(self, request):
        return render(request, "post.html")
    def post(self, request):
        if request.user.is_authenticated:
            data = request.POST
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_path = fs.path(filename)
            note = models.Post()
            match = re.fullmatch(r'[^$]*[.](png|jpg|jpeg)$', filename)
            if match is None:
                return HttpResponse("Вы должны выбрать фото расширения .png .jpg или .jpeg")
            else:
                note.create_post(image=filename, title=data['title'], text=data['text'], topic=data['topic'], date=datetime.datetime.now(), author=request.user.username)
                return redirect('/home')


class About(View):
    def get(self, request):
        return render(request, "about.html")


class Contacts(View):
    def get(self, request):
        return render(request, "contact.html")


class Auth(View):
    def get(self, request):
        return render(request, "authorization.html")
    def post(self, request):
        data = request.POST
        user = authenticate(request, username=data["name"], password=data["password"])
        if user is None:
            return HttpResponseBadRequest("Неверный пароль или имя пользователя")
        else:
            login(request, user)
            return redirect("/home")


class Register(View):
    def get(self, request):
        return render(request, "reg.html")
    def post(self, request):
        data = request.POST
        name = data['name']
        password = data['password']
        password_check = data['password_check']
        email = data["email"]
        if password == password_check:
            user = models.NoteUser()
            user.create_user(username=name, password=password, email=email)
            return redirect('/home')
        else:
            return HttpResponseBadRequest("Пароли не совпадают!")


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('/home')
        else:
            return HttpResponse(AUTH_REQUIRED_MSG)


class Profile(View):
    def get(self, request):
        posts = models.Post.objects.filter(author=request.user.username)
        return render(request, "profile.html", {"articles": posts, "username": request.user.username})
    def post(self, request):
        data = request.POST
        models.Post.objects.filter(id=data['id']).delete()
        return redirect("/profile")


class Rename(View):
    def get(self, request):
        return render(request, "rename.html")
    def post(self, request):
        data = request.POST
        user = authenticate(request, username=request.user.username, password=data["password"])
        if user is None:
            return HttpResponseBadRequest("Неверный пароль!")
        else:
            models.NoteUser.objects.filter(username=request.user.username).update(username=data["name"])
            models.Post.objects.filter(author=request.user.username).update(author=data["name"])
            return redirect("/profile")


class ChangePassword(View):
    @sync_to_async
    def get(self, request):
        if request.user.is_authenticated:
            email = request.user.email
            code = random.randint(1000, 9999)
            message = f"Ваш код подтверждения: {code}. Никому не сообщайте этот код!"
            email_code.send_email(message=message, receiver=email)
            models.NoteUser.objects.filter(username=request.user.username).update(code=code)
            return render(request, "repassword.html")
        else:
            return HttpResponse(AUTH_REQUIRED_MSG)

    @sync_to_async
    def post(self, request):
        data = request.POST
        code = request.user.code

        if data["password"] == data["password_check"] and data["code"] == str(code):
            user = request.user
            print(request.user.username)
            user.set_password(data["password"])
            user.save()
            return redirect("/home")
        else:
            return HttpResponse("Неверный код подтверждения или пароли не совпадают!")
