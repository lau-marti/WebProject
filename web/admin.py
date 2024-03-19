from django.contrib import admin

# This is how you can register your models with the Django admin so that you can manage them from the admin interface

from .models import Song, Artist, Genre

admin.site.register(Song)
admin.site.register(Artist)
admin.site.register(Genre)

