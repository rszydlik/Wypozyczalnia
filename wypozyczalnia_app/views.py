from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, ListView

from wypozyczalnia_app.forms import BookForm, AddUserForm, ChangePasswordForm, Login
from wypozyczalnia_app.models import Book
from django.contrib.auth.models import User


# Create your views here.

# books

class AddBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'index.html'
    success_url = reverse_lazy('home')


class BookListView(ListView):
    model = Book
    template_name = 'show.html'


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


# users

class LogIn(View):

    def get(self, request):
        form = Login()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = Login(request.POST)
        if form.is_valid():
            login_form = form.cleaned_data['login_form']
            password = form.cleaned_data['password']
            user = authenticate(username=login_form, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form = Login()
                return render(request, 'login.html', {'form': form})
        else:
            form = Login()
            return render(request, 'login.html', {'form': form})


class LogOut(View):

    def get(self, request):
        logout(request)
        user = None
        return redirect("home")


class AddUser(FormView):
    template_name = 'add_user.html'
    form_class = AddUserForm
    success_url = reverse_lazy('list-users')

    def form_valid(self, form):
        form.save()
        return super(AddUser, self).form_valid(form)


class ListUsers(ListView):
    model = User
    template_name = 'user_list.html'


class ChangePassword(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    permission_required = 'users.change_user'
    template_name = 'add_user.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user.id
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super(ChangePassword, self).form_valid(form)


# user's library

class UserBookView(ListView):
    template_name = 'show_library.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Book.objects.filter(owners=user)
        return queryset


def addtouser(request, bookid):
    book = Book.objects.get(id=bookid)
    book.owners.add(request.user)
    book.save()
    return redirect('home')


def removefromuser(request, bookid):
    book = Book.objects.get(id=bookid)
    book.owners.remove(request.user)
    book.save()
    return redirect('home')
