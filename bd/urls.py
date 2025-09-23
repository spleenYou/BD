"""
URL configuration for bd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
import authentication.views as authentication
import my_library.views as library
import bd.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('under_construction/', bd.views.under_construction, name='site_under_construction'),
    path('', library.home, name='home'),
    path('login/', authentication.login_page, name='login'),
    path('logout/', authentication.logout_page, name='logout'),
    path('signup/', authentication.signup_page, name='signup'),
    path('account/', authentication.account, name='account'),
    path('my_library/', library.my_library, name='my_library'),
    path('my_library/serie/<int:serie_id>', library.view_serie, name='view_serie'),
    path('my_library/book/add/', library.add_book, name='my_library_add_book'),
    path(
        'my_library/serie/<int:serie_id>/book/add/',
        library.add_book_serie,
        name='my_library_add_book_serie'
    ),
    path('my_library/book/del/<int:book_id>', library.del_book, name='my_library_del_book'),
    path(
        'book/add/<int:book_id>',
        library.add_book_isbn,
        name='add_book_isbn'
    ),
    path('book/<int:book_id>/author/add', library.add_author_to_book, name='add_author_to_book'),
    path('book/<int:book_id>/author/del/<int:author_id>', library.del_author_to_book, name='del_author_to_book'),
    path('book/<int:book_id>/publisher/add', library.add_publisher_to_book, name='add_publisher_to_book'),
    path('book/<int:book_id>/publisher/del', library.del_publisher_to_book, name='del_publisher_to_book'),
    path('favicon.ico', lambda x: redirect('/static/icons/favicon.ico')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
