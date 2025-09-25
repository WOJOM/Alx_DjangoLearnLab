from rest_framework import serializers
from django.utils.timezone import now
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Includes validation to ensure the publication year is not in the future.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value):
        current_year = now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes a nested serializer for books (one-to-many relationship).
    """
    books = BookSerializer(many=True, read_only=True)  # Nested serialization

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
