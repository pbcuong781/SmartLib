from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth


#HOMEPAGE
def index(request):
    return render(request,'index.html')

#
def signup(request):
    if request.method == 'POST':
        firstname = request.POST['signup-firstname']
        lastname = request.POST['signup-lastname']
        username = request.POST['signup-username']
        email = request.POST['signup-email']
        password = request.POST['signup-pass']
        confirmPassword = request.POST['signup-confirm-pass']
        #Kiem tra mat khau co trung khop hay khong
        if password == confirmPassword:
            
            if User.objects.filter(username = username).exists(): #kiem tra trong database xem da ton tai username nay chua
                messages.info(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email = email).exists(): #kiem tra trong database xem email da duoc dung chua
                messages.info(request, 'Email Taken')
                return redirect('signup')
            else:
                messages.info(request, 'Sign up successful') #neu khong thi tao tai khoan roi them vao database
                user = User.objects.create(username = username, first_name=firstname, last_name=lastname, email = email, password = password)
                user.set_password(password)
                user.save()
        else:
            messages.info(request, 'Password not matching...')
            return redirect('signup')
        return redirect('login1')
    else :
        
        return render(request, 'registration/signup.html')

def login1(request):
    if request.method == 'POST':
        name = request.POST['login-name']
        password = request.POST['login-pass']
        user = authenticate(username = name, password = password) #kiem tra tai khoan dang nhap
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login1')
    else:
        return render(request, 'registration/login1.html')

def logout1(request):
    auth.logout(request)
    return redirect('/')

def BookListView(request):
    book_list = Book.objects.all()  #lay ra toan bo du lieu trong bang book
    total = Book.objects.filter().count()  #dem so sach co trong bang
    return render(request, 'catalog/book_list.html', locals())

@login_required
def BookCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES) #tao form them moi sach
        if form.is_valid():
            form.save()
            return redirect('books')
    return render(request, 'catalog/form.html', locals())


@login_required
def BookUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    book = Book.objects.get(title=pk)
    form = BookForm(instance=book)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=book) #tao form voi nhung thong tin cu cua sach de update
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('books')
    return render(request, 'catalog/form.html', locals())


@login_required
def BookDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    book=Book.objects.get(title=pk) #xoa sach
    book.delete()
    return redirect('books')

@login_required
def BookBorrow(request, pk):
    book=Book.objects.filter(title=pk).update(available_borrow=0)
    title = Book.objects.get(title = pk)
    username=request.user
    bookBorrow = BookBorrowed.objects.create(title=title, username=username)
    bookBorrow.save()
    return redirect('books')

@login_required
def BookBorrowedListView(request):
    book_list = BookBorrowed.objects.filter(username = request.user)
    return render(request, 'catalog/book_list_borrow.html', locals())

@login_required
def BookReturn(request, pk):
    book = Book.objects.filter(title=pk)[0]
    BookBorrowed.objects.filter(title=book).update(date_return=datetime.date.today())
    Book.objects.filter(title=pk).update(available_borrow=1)
    return redirect('mybooks')

def NotificationView(request):
    noti_list = Notification.objects.filter(username=request.user)
    print(noti_list)
    # MODELNAME.objects.all() is used to get all objects i.e. tuples from database
    return render(request, 'catalog/notification_list.html', locals())

import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title','author'])
       
        book_list= Book.objects.filter(entry_query)
        total = Book.objects.filter(entry_query).count()
    return render(request,'catalog/book_list.html',locals() )

def search_book_borrow(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title'])
        books= Book.objects.filter(entry_query)
        book_list = []
        for book in books:
            bookbrs = BookBorrowed.objects.filter(title=book, username=request.user)
            for bookbr in bookbrs:
                book_list.append(bookbr)
    return render(request,'catalog/book_list_borrow.html',locals() )

