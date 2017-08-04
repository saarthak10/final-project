# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models

# Create your models here.
class UserModel(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 120)
    password = models.CharField(max_length = 40)
    created_on = models.DateTimeField(auto_now = True)
    updated_on = models.DateTimeField(auto_now = True)


class Session_token(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)


    def create_token(self):
        self.session_token = uuid.uuid4()

class PostModel(models.Model):
    user = models.ForeignKey(UserModel)
    image = models.FileField(upload_to = "user_images")
    image_url = models.CharField(max_length = 100)
    caption = models.CharField(max_length = 300)
    created_on = models.DateTimeField(auto_now =True)
    updated_on = models.DateTimeField(auto_now_add = True)
    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post = self))
class LikeModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)



class CommentModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    comment_text = models.CharField(max_length = 800)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)