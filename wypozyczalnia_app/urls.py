from django.urls import path, include
from wypozyczalnia_app import views
from wypozyczalnia_app.views import AddUser, ListUsers, AddBookView, BookListView, UserBookView, \
    ChangePassword, FriendsList, FriendDetail, FriendCreate, FriendUpdate, FriendDelete, AllThingsView

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
    # friendlist
    path('friends/list/', FriendsList.as_view(), name='friend-list'),
    path('friends/detail/', FriendDetail.as_view(), name='friend-detail'),
    path('friends/create/', FriendCreate.as_view(), name='friend-create'),
    path('friends/update/', FriendUpdate.as_view(), name='friend-update'),
    path('friends/delete', FriendDelete.as_view(), name='friend-delete')
]
