from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.LikeCount)
admin.site.register(models.LikeRecord)
