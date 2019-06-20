from django.contrib import admin
from .models import Post, Event


class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "date_posted",)


admin.site.register(Post, PostAdmin)
admin.site.register(Event)

