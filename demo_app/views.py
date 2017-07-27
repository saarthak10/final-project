# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,HttpResponseRedirect,redirect
from forms import SignUpForm
from models import UserModel
import datetime

def signup_view(request):
    today = datetime.datetime.now()
    
    return render(request,'index.html',{'today': today})
    if request.method == "POST":
        form = SignUpForm(request.Post)
        if form.is_valid():
            username = form.cleaned_data["username"]
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = UserModel(username = username ,name = name,email = email,password = make_password(password))
            user.save()
            return HttpResponseRedirect('/register/success')
    elif request.method == "GET":
        signup_form = SignUpForm()
        return render(request, "index.html",{'signup_form':signup_form})

def register_success(request):
    return render(request,'success.html')