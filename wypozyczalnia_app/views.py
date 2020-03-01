from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, ListView, DetailView, UpdateView, DeleteView
import requests

from Wypozyczalnia.local_settings import geoapi
from wypozyczalnia_app.forms import BookForm, AddUserForm, ChangePasswordForm, Login, FriendForm, LendForm
from wypozyczalnia_app.models import Book, Friend, Library
from django.contrib.auth.models import User


# Create your views here.
class AllThingsView(View):

    def get(self, request):
        num_books = Book.objects.all().count()
        num_users = User.objects.all().count()
        num_libraries = Library.objects.all().count()
        num_friends = Friend.objects.all().count()
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '37.7.70.21')
        response = requests.get('http://api.ipstack.com/' + ip_address + '?access_key=' + geoapi + '&format=1')
        geodata = response.json()
        context = {
            'num_books': num_books,
            'num_users': num_users,
            'num_libraries': num_libraries,
            'num_friends': num_friends,
            'ip': geodata['ip'],
            'country': geodata['country_name']
        }

        return render(request, 'home.html', context=context)


# books

class AddBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'index.html'
    success_url = reverse_lazy('booklist')


class BookListView(ListView):
    model = Book
    template_name = 'show.html'


class BookUpdate(UpdateView):
    model = Book
    fields = ['btitle', 'bauthor', 'bdescription']
    template_name = 'wypozyczalnia_app/friend_form.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'form'
    success_url = reverse_lazy('booklist')


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('booklist')


# users

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
    template_name = 'wypozyczalnia_app/show_library.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Library.objects.filter(owner=user)
        return queryset


def addtouser(request, bookid):
    book = Book.objects.get(id=bookid)
    book.owners.add(request.user)
    book.save()
    return redirect('show')


def removefromuser(request, bookid):
    book = Book.objects.get(id=bookid)
    book.owners.remove(request.user)
    book.save()
    return redirect('show')


class Lend(UpdateView):
    model = Library
    form_class = LendForm
    template_name = "wypozyczalnia_app/lend.html"
    success_url = reverse_lazy('show')

    def get_form_kwargs(self):
        kwargs = super(Lend, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


def regain(request, libraryid):
    library = Library.objects.get(id=libraryid)
    library.borrower = None
    library.save()
    return redirect('show')


# friends

class FriendsList(ListView):
    model = Friend
    template_name = 'wypozyczalnia_app/friend_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Friend.objects.filter(relates=user)
        return queryset


class FriendDetail(DetailView):
    model = Friend
    fields = ['name', 'email', 'phone']
    template_name = 'wypozyczalnia_app/friend_form.html'
    pk_url_kwarg = 'pk'


class FriendCreate(CreateView):
    model = Friend
    form_class = FriendForm
    template_name = 'wypozyczalnia_app/friend_form.html'
    success_url = reverse_lazy('friend-list')

    def form_valid(self, form):
        friend = form.save(commit=False)
        friend.relates = self.request.user
        return super(FriendCreate, self).form_valid(form)


class FriendUpdate(UpdateView):
    model = Friend
    fields = ['name', 'email', 'phone']
    template_name = 'wypozyczalnia_app/friend_form.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'form'
    success_url = reverse_lazy('friend-list')


class FriendDelete(DeleteView):
    model = Friend
    success_url = reverse_lazy('friend-list')
