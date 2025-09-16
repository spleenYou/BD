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
import authentication.views
import my_library.views as library
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', library.home, name='home'),
    path('login/', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_page, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('account/', library.account, name='account'),
    path('my_library/', library.my_library, name='my_library'),
    path('my_library/serie/<int:serie_id>', library.view_serie, name='view_serie'),
    path('my_library/book/add/', library.add_book, name='my_library_add_book'),
    path(
        'my_library/book/add/<int:book_id>',
        library.add_book_isbn,
        name='my_library_add_book_isbn'
    ),
    path(
        'my_library/serie/<int:serie_id>/book/add/',
        library.add_book_serie,
        name='my_library_add_book_serie'
    ),
    path('my_library/book/del/<int:book_id>', library.del_book, name='my_library_del_book'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
