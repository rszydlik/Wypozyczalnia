"""Wypozyczalnia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wypozyczalnia_app import views
from wypozyczalnia_app.views import LogIn, LogOut, AddUser, ListUsers, AddBookView, BookListView, UserBookView, \
    ChangePassword

urlpatterns = [
    # administration
    path('admin', admin.site.urls),
    # books
    path('addbook', AddBookView.as_view(), name='addbook'),
    path('', BookListView.as_view(), name='booklist'),
    path('update/<int:bookid>', views.updatebook),
    path('delete/<int:bookid>', views.destroybook),
    # users
    path('login/', LogIn.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('add_user/', AddUser.as_view(), name='add-user'),
    path('list_users/', ListUsers.as_view(), name='list-users'),
    path('changepassword/', ChangePassword.as_view(), name='change-password'),
    # user's library
    path('show', UserBookView.as_view(), name='home'),
    path('addtolibrary/<int:bookid>', views.addtouser),
    path('removefromlibrary/<int:bookid>', views.removefromuser),
]
