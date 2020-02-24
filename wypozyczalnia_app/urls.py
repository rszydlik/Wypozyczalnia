from django.urls import path, include
from wypozyczalnia_app import views
from wypozyczalnia_app.views import AddUser, ListUsers, AddBookView, BookListView, UserBookView, FriendsList, \
    FriendDetail, FriendCreate, FriendUpdate, FriendDelete, AllThingsView, Lend

urlpatterns = [
    path('', AllThingsView.as_view(), name='home'),
    # books
    path('addbook', AddBookView.as_view(), name='addbook'),
    path('books', BookListView.as_view(), name='booklist'),
    path('update/<int:bookid>', views.updatebook),
    path('delete/<int:bookid>', views.destroybook),
    # users
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_user/', AddUser.as_view(), name='add-user'),
    path('list_users/', ListUsers.as_view(), name='list-users'),
    # path('changepassword/', ChangePassword.as_view(), name='change-password'),
    # user's library
    path('show', UserBookView.as_view(), name='show'),
    path('addtolibrary/<int:bookid>', views.addtouser),
    path('removefromlibrary/<int:bookid>', views.removefromuser),
    path('lend/<int:pk>', Lend.as_view(), name='lend'),
    path('regain/<int:libraryid>', views.regain),
    # friendlist
    path('friends/list/', FriendsList.as_view(), name='friend-list'),
    path('friends/detail/<int:pk>', FriendDetail.as_view(), name='friend-detail'),
    path('friends/create/', FriendCreate.as_view(), name='friend-create'),
    path('friends/update/<int:friendid>', FriendUpdate.as_view(), name='friend-update'),
    path('friends/delete/<int:friendid>', FriendDelete.as_view(), name='friend-delete')
]
