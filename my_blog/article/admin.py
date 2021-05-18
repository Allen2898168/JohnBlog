from django.contrib import admin

# Register your models here.
from .models import ArticlePost
admin.site.register(ArticlePost)
admin.site.site_title = "后台管理系统"
