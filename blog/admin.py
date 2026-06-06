from django.contrib import admin
from blog import models

# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'created_date', 'owner'