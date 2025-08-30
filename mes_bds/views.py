from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import Serie, Book


def home(request):
    member_list = None
    if request.user.is_authenticated:
        member_list = [request.user.username.capitalize()]
    return render(request, 'mes_bds/index.html', {'member_list': member_list})


@login_required
def account(request):
    return render(request, 'mes_bds/account.html')


@login_required
def my_library(request):
    user = request.user
    library = Serie.objects.filter(
        books__book__user=user
    ).prefetch_related(
        Prefetch('books', queryset=Book.objects.filter(book__user=user).order_by('number'))
    ).distinct()
    return render(request, 'mes_bds/my_library.html', {'library': library})
