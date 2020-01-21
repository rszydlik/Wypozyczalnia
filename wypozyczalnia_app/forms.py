from django import forms
from wypozyczalnia_app.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
