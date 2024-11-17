from django.contrib import admin
from .models import User, Topic, Post

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Post)
