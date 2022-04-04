"""SmartLib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include,re_path
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login1, name='login1'),
    path('logout/', views.logout1, name='logout1'),

    path('books/', views.BookListView, name='books'),
    path('book/create/', views.BookCreate, name='book_create'),
    path('book/<str:pk>/update/', views.BookUpdate, name='book_update'),
    path('book/<str:pk>/delete/', views.BookDelete, name='book_delete'),
    path('book/<str:pk>/borrow/', views.BookBorrow, name='book_borrow'),
    path('mybooks/', views.BookBorrowedListView, name='mybooks'),
    path('notifications/', views.NotificationView, name='notifications'),
    path('mybooks/<str:pk>/return/', views.BookReturn, name='book_return'),
    re_path(r'^search_b/', views.search_book, name="search_b"),
    re_path(r'^search_b_b/', views.search_book_borrow, name="search_b_borrow"),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
