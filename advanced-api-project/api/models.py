from django.db import models

# Create your models here.

from django.db import models
from django.utils.timezone import now

class Author(models.Model):
    """
    Represents an author of one or more books.
    Each author can be linked to multiple books.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book written by an author.
    Each book belongs to exactly one author (ForeignKey).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
