from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Count, Q, Exists, OuterRef, ExpressionWrapper, BooleanField, F, Case, When, Value
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
def add_book_serie(request, serie_id):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        book = Book.objects.get(pk=book_id)
        library = Library.objects.create(
            user=request.user,
            book=book
        )
        library.save()
        return redirect('my_library')
    books = Book.objects.filter(serie_id=serie_id).annotate(
        is_owned=Exists(
            Library.objects.filter(
                book=OuterRef('pk'),
                user=request.user
            )
        )
    )
    return render(request, 'library/add_book_serie.html', {'books': books})


@login_required
def add_book(request):
    user = request.user
    series = Serie.objects.filter(books__isnull=False).annotate(
        total_books=Count('books', distinct=True),
        owned_books=Count('books', filter=Q(books__book__user=user))
    ).annotate(
        is_complete=Case(
            When(total_books=F('owned_books'), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).filter(
        is_complete=False
    )
    print(series)
    return render(request, 'library/add_book.html', {'series': series})


@login_required
def my_library(request):
    user = request.user
    library = Serie.objects.all().annotate(
        total_books=Count('books', distinct=True),
        owned_books=Count('books', filter=Q(books__book__user=user), distinct=True),
    ).annotate(
        is_complete=Case(
            When(total_books=F('owned_books'), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).filter(
        books__book__user=user
    ).prefetch_related(
        Prefetch('books', queryset=Book.objects.filter(book__user=user).order_by('number'))
    ).distinct()
    return render(request, 'library/my_library.html', {'library': library})
