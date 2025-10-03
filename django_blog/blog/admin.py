
# Register your models here.
from django.contrib import admin
from .models import Profile, Post

admin.site.register(Profile)
admin.site.register(Post)


from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content',)
