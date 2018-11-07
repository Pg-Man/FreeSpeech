from django.contrib import admin

# Register your models here.
from .models import Mood,Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('nickname','message','enabled','pub_time')
    ordering = ('-pub_time',)
admin.site.register(Mood)
admin.site.register(Post,PostAdmin)