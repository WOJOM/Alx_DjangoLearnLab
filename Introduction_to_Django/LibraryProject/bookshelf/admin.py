
# Register your models here.
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # What fields show up in the admin list view
    list_display = ('title', 'author', 'publication_year')

    # Add filters for easy navigation
    list_filter = ('publication_year', 'author')

    # Enable search functionality
    search_fields = ('title', 'author')
