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
import mes_bds.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mes_bds.views.home, name='home'),
    path('login/', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_page, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('account/', mes_bds.views.account, name='account'),
    path('my_library/', mes_bds.views.my_library, name='my_library'),
    path('add_book/', mes_bds.views.add_book, name='add_book'),
]
