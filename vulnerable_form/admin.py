from django.contrib import admin
from .models import Comment
from .protected_models import XSSProtectedComment

# Register your models here.
admin.site.register(Comment)
admin.site.register(XSSProtectedComment)
