from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

# Already existing BookList view here (optional, you can keep it)

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard CRUD operations for the Book model
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
