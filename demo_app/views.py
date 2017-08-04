# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from imgurpython import ImgurClient
import datetime
from django_project.settings import BASE_DIR
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from forms import *
from models import *


def signup_view(request):
    today = datetime.datetime.now()
    

    if request.method == "POST":

        form = SignUpForm(request.POST)

        if form.is_valid():
                username = form.cleaned_data["username"]
                name = form.cleaned_data["name"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]

                #validation of user data
                #if len(username)!= 0 and len(name)!= 0 :

                if len(username) <= 4 and len(password)<=5:

                    user = UserModel(username = username ,name = name,email = email,password = make_password(password))
                    user.save()

                #Sending an email to the user for confirmation of signing up
                    send_mail("Sign up confirmed","Welcome to the swach bharat campaign", from_email= settings.EMAIL_HOST_USER,recipient_list= [email],fail_silently=True)

                    return render(request,"success.html")

                else:
                    print("line 36")
                    return render(request,'error.html')
    elif request.method == "GET":
        signup_form = SignUpForm()

        return render(request, "index.html",{'signup_form':signup_form,'today':today})

def login_view(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = UserModel.objects.filter(username).first()

            if user:
                #check whether th epassword is correct or not
                if check_password(password,user.password):
                    token = Session_token(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session token' , value = token.session_token)
                    return response

                else:
                    message = "enter correct password"
                    return render(request,'login.html',{'message':message})
            else:
                message = "user does not exist"
                return render(request,'login,html',{'message':message})


    elif request.method == 'GET':
        form = LogInForm()
        return render(request,'login.html',{'form':form})
def check_validation(request):
    if request.Cookies.get('session_token'):
        session = Session_token.objects.filter(session_token = request.Cookies.get('session_token')).first()
        if session:
            return session.user
        else:
            return None

def post_view(request):
    user = check_validation(request)
    if user:
        if request.method == "GET":
            form = PostForm(request)
            return render(request,"post.html",{'form':form})
        elif request.method == "POST":
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user = user,image = image,caption = caption)

                path = str(BASE_DIR + post.image_url)
                client = ImgurClient('938471fc0a35a36','e87b9bc6fb6b69a333d03f7933fd283e712da0c3' )
                post.image_url = client.upload_from_path(path , anon=True)['link']
                post.save()

    else:
        redirect('login/')


def like_view(request):
    user  = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid(request):
            post_id = form.cleaned_data.get('post').id
            existing_like = form.objects.filter(post_id = post_id,user = user).first()
            if not existing_like:
                 LikeModel.objects.create(post_id=post_id,user = user)

            else:
                existing_like.delete()
            return redirect('feed/')

    else:
        return redirect('/login/')


def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('-created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id = post.id,user = user).first()
            if existing_like:
                post.has_liked = True
        return render(request,'feed.html',{'post': posts})
    else:
       return  redirect('/login/')\

def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel(user = user , post_id = post_id,comment_text = comment_text)
            comment.save()
            return redirect('feed/')
        else:
            return redirect('feed/')
    else:
        return redirect('login/')
