# bookshelf/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_date"]

class BookSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Search title or author"})
    )

    def clean_q(self):
        q = self.cleaned_data.get("q", "")
        # Additional sanitization if needed
        return q.strip()
