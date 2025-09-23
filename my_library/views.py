from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import (
    Prefetch,
    Count,
    Q,
    BooleanField,
    F,
    Case,
    When,
    Value
)
from .models import Serie, Book, Library, Author, Publisher
from .api import get_book_info, get_serie_name
from .img import save_book_cover
from .forms import AddBookForm


def home(request):
    member_list = None
    if request.user.is_authenticated:
        member_list = [request.user.username.capitalize()]
    return render(request, 'my_library/index.html', {'member_list': member_list})


@login_required
def add_book_isbn(request, book_id):
    book = Book.objects.get(pk=book_id)
    form = AddBookForm(instance=book)
    if request.method == 'POST':
        form = AddBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            if request.POST['validation'] == 'true':
                Library.objects.create(
                    user=request.user,
                    book_id=book_id
                )
            return redirect('my_library')
    return render(
        request=request,
        template_name='my_library/add_book_isbn.html',
        context={'form': form, 'book': book}
    )


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
        return redirect('view_serie', serie_id)
    books = Book.objects.filter(serie__id=serie_id).exclude(
        id__in=Library.objects.filter(user=request.user).values_list('book_id', flat=True)
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
                if book_id is not None:
                    return redirect('add_book_isbn', book_id=book_id)
                else:
                    messages.error(request, message='Erreur du serveur')
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
    if book_info is not None:
        serie_name = get_serie_name('https://www.bdbase.fr/recherche?sch=' + isbn)
        serie = Serie.objects.filter(name=serie_name).first()
        if not serie:
            serie = Serie.objects.create(name=serie_name)
        new_book = Book(
            title=book_info['title'],
            ISBN=book_info['isbn'],
            serie=serie,
            first_publish_year=book_info['first_publish_year']
        )
        new_book.save()
        save_book_cover(new_book, book_info['cover_edition_key'])
        new_book.authors.set(find_author(book_info['author_name']))
        return new_book.id
    return None


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
    ).filter(
        books__book__user=user
    )
    return render(request, 'my_library/my_library.html', {'library': library})


@login_required
def del_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        serie_id = book.serie.id
        if request.POST['validation'] == 'true':
            book_to_remove = Library.objects.filter(book=book, user=request.user)
            book_to_remove.delete()
        return redirect('view_serie', serie_id)
    return render(request, 'my_library/del_book.html', {'book': book})


@login_required
def view_serie(request, serie_id):
    user = request.user
    serie = Serie.objects.filter(pk=serie_id).annotate(
        total_books=Count('books', distinct=True),
        owned_books=Count('books', filter=Q(books__book__user=user), distinct=True),
    ).annotate(
        is_complete=Case(
            When(total_books=F('owned_books'), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).prefetch_related(
        Prefetch('books', queryset=Book.objects.filter(book__user=user).order_by('number'))
    ).first()
    return render(request, 'my_library/view_serie.html', {'serie': serie})


@login_required
def add_author_to_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        if 'add' in request.POST and request.POST['author'] != '':
            new_author = Author.objects.create(name=request.POST['author'])
            new_author.save()
        else:
            new_author = Author.objects.get(pk=request.POST['author'])
        book.authors.add(new_author)
        return redirect('add_book_isbn', book.id)
    authors = Author.objects.all().exclude(
        id__in=book.authors.all().values_list('id', flat=True)
    )
    return render(request, 'my_library/add_author_to_book.html', {'book': book, 'authors': authors})


@login_required
def del_author_to_book(request, book_id, author_id):
    book = Book.objects.get(pk=book_id)
    author = Author.objects.get(pk=author_id)
    book.authors.remove(author)
    return redirect('add_book_isbn', book_id)


@login_required
def add_publisher_to_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        if 'add' in request.POST and request.POST['publisher'] != '':
            new_publisher = Publisher.objects.create(name=request.POST['publisher'])
            new_publisher.save()
        else:
            new_publisher = Publisher.objects.get(pk=request.POST['publisher'])
        book.publisher = new_publisher
        book.save()
        return redirect('add_book_isbn', book.id)
    publishers = Publisher.objects.all()
    return render(request, 'my_library/add_publisher_to_book.html', {'book': book, 'publishers': publishers})


@login_required
def del_publisher_to_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.publisher = None
    book.save()
    return redirect('add_book_isbn', book_id)
