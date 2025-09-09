from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Count, Q, Exists, OuterRef
from .models import Serie, Book, Library
from . import forms


def home(request):
    member_list = None
    if request.user.is_authenticated:
        member_list = [request.user.username.capitalize()]
    return render(request, 'library/index.html', {'member_list': member_list})


@login_required
def account(request):
    return render(request, 'library/account.html')


@login_required
def add_book_isbn(request):
    form = forms.AddBookForm()
    return render(request, 'library/add_book_isbn.html', {'form': form})


@login_required
def add_book_serie(request):
    return render(request, 'library/add_book.html')


@login_required
def add_book(request):
    user = request.user
    if request.method == 'POST':
        print(request.POST)
        # if 'serie' in request.POST:
        #     selected_serie_id = request.POST['serie']
        #     books = Book.objects.filter(serie=selected_serie_id).annotate(
        #         is_owned=Exists(
        #             Library.objects.filter(
        #                 book=OuterRef('pk'),
        #                 user=user
        #             )
        #         )
        #     )
        #     serie = Serie.objects.get(id=selected_serie_id)
        #     return render(request, 'library/select_book.html', {'books': books, 'serie': serie})
        # if 'book' in request.POST:
        #     selected_book_id = request.POST['book']
        #     selected_book = Book.objects.get(pk=selected_book_id)
        #     new_library = Library.objects.create(
        #         user=user,
        #         book=selected_book
        #     )
        #     new_library.save()
        #     return redirect('my_library')
    series = Serie.objects.all().annotate(
        total_books=Count('books', distinct=True),
        owned_books=Count('books', filter=Q(books__book__user=user))
    )
    return render(request, 'library/add_book.html', {'series': series})


@login_required
def my_library(request):
    user = request.user
    library = Serie.objects.filter(
        books__book__user=user
    ).prefetch_related(
        Prefetch('books', queryset=Book.objects.filter(book__user=user).order_by('number'))
    ).distinct()
    return render(request, 'library/my_library.html', {'library': library})
