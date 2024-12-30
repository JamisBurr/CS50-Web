from django.contrib import admin
from .models import User, Post

# Register the User model
admin.site.register(User)

# Register the Post model
admin.site.register(Post)
