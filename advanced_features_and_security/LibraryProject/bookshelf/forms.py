from django import forms
from .models import Book


class ExampleForm(forms.ModelForm):
    """
    ExampleForm demonstrates safe handling of user input
    to prevent SQL injection and XSS attacks.
    """

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date']

    def clean_title(self):
        """
        Example of input sanitization/validation.
        Prevents malicious script injection.
        """
        title = self.cleaned_data.get("title")
        if "<script>" in title.lower():
            raise forms.ValidationError("Invalid input detected.")
        return title
