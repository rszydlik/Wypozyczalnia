from django.shortcuts import render, redirect
from wypozyczalnia_app.forms import BookForm
from wypozyczalnia_app.models import Book


# Create your views here.
def addbook(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = BookForm()
    return render(request, 'index.html', {'form': form})


def showbook(request):
    books = Book.objects.all()
    return render(request, 'show.html', {'books': books})


def editbook(request, bookid):
    book = Book.objects.get(id=bookid)
    return render(request, 'edit.html', {'book': book})


def updatebook(request, bookid):
    book = Book.objects.get(id=bookid)
    form = BookForm(request.POST, instance=bookid)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, 'edit.html', {'book': book})


def destroybook(request, bookid):
    book = Book.objects.get(id=bookid)
    book.delete()
    return redirect("/show")
