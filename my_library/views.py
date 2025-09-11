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
from .models import Serie, Book, Library, Author
from .api import get_book_info


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
def add_book(request):
    if request.method == 'POST':
        isbn = request.POST['isbn']
        isbn = isbn.replace('-', '').replace(' ', '')
        if is_isbn(isbn):
            if not isbn_in_db(isbn):
                book_id = fill_db_book(isbn)
                return redirect(to='my_library_add_book_isbn', book_id=book_id)
            else:
                messages.error(request, message='Livre déjà ajouté')
        else:
            messages.error(request, message='isbn invalide')
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
    return render(request, template_name='my_library/add_book.html', context={'series': series})


def isbn_in_db(isbn):
    result = Book.objects.filter(ISBN=isbn).first()
    if result is not None:
        return True
    return False


def is_isbn(isbn):
    return isbn.isdigit() and (len(isbn) == 10 or len(isbn) == 13)


def fill_db_book(isbn):
    book_info = get_book_info(isbn)
    new_book = Book(
        title=book_info['title'],
        ISBN=book_info['isbn'],
        cover_ID=book_info['cover_edition_key'],
        serie=Serie.objects.get(name='Unsorted'),
    )
    new_book.save()
    new_book.authors.set(find_author(book_info['author_name']))
    return new_book.id


def find_author(author_names):
    author_tab = []
    for author_name in author_names:
        author = Author.objects.filter(name=author_name).first()
        if author is None:
            new_author = Author.objects.create(name=author_name)
            author = new_author.save()
        author_tab.append(author)
    return author_tab


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
