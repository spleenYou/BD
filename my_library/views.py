from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import (
    Prefetch,
    Count,
    Q,
    Exists,
    OuterRef,
    BooleanField,
    F,
    Case,
    When,
    Value
)
from .models import Serie, Book, Library


def home(request):
    member_list = None
    if request.user.is_authenticated:
        member_list = [request.user.username.capitalize()]
    return render(request, 'my_library/index.html', {'member_list': member_list})


@login_required
def account(request):
    return render(request, 'my_library/account.html')


@login_required
def add_book_isbn(request, book_id):
    if request.method == 'POST':
        if request.POST['validation'] == 'true':
            Library.objects.create(
                user=request.user,
                book_id=book_id
            )
        return redirect('my_library')
    book = Book.objects.filter(pk=book_id).annotate(
        already_owned=Exists(
            Library.objects.filter(
                book_id=book_id,
                user=request.user
            )
        )
    ).first()
    if book.already_owned:
        messages.info(request, 'Livre déjà dans votre collection')
    return render(request, 'my_library/add_book_isbn.html', {'book': book})


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
    return render(request, 'my_library/add_book_serie.html', {'books': books})


@login_required
def add_book(request, error=None):
    if request.method == 'POST':
        ISBN = request.POST['ISBN']
        ISBN = ISBN.replace('-', '').replace(' ', '')
        if not (ISBN.isdigit() and (len(ISBN) == 10 or len(ISBN) == 13)):
            messages.error(request, 'ISBN invalide')
            return redirect('my_library_add_book')
        else:
            ISBN_checked, book_info = check_ISBN(ISBN)
            if ISBN_checked:
                book_id = fill_db_book(book_info)
                return redirect('my_library_add_book_isbn', book_id=book_id)
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
    return render(request, 'my_library/add_book.html', {'series': series})


def check_ISBN(ISBN):
    return True, {'test': 'test'}


def fill_db_book(book_info):
    print(book_info)
    return 1


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
    return render(request, 'my_library/my_library.html', {'library': library})


@login_required
def del_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        if request.POST['validation'] == 'true':
            book_to_remove = Library.objects.filter(book=book, user=request.user)
            book_to_remove.delete()
        return redirect('my_library')
    return render(request, 'my_library/del_book.html', {'book': book})
