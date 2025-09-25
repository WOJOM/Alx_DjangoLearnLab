from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


# ListView: anyone can see all books
class BookListView(generics.ListAPIView):
    """
    GET /books/
    Returns a list of all books.
    Read-only access is allowed to unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # no login required


# DetailView: anyone can see one book
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<id>/
    Returns details of a single book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# CreateView: only authenticated users can create books
class BookCreateView(generics.CreateAPIView):
    """
    POST /books/create/
    Creates a new book (auth required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# UpdateView: only authenticated users can update
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /books/<id>/update/
    Updates an existing book (auth required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# DeleteView: only authenticated users can delete
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<id>/delete/
    Deletes a book (auth required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # ✅ Filtering fields
    filterset_fields = ['title', 'author__name', 'publication_year']

    # ✅ Search fields
    search_fields = ['title', 'author__name']

    # ✅ Ordering fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering
