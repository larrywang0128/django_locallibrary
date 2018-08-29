# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 00:06:52 2018

@author: haiwa
"""

from django.urls import path
from . import views

# define URL patterns for catalog app
urlpatterns = [
        ## views.index — a function named index() in views.py
        ## The name argument uniquely identifies this particular URL mapping. 
        ## You can use this name to "reverse" the mapper — to dynamically create a URL pointing to the resource the mapper is designed to handle.
        ## e.g. <a href="{% url 'index' %}">Home</a> creates a link to index page without hardcoding
        path('', views.index, name='index'),
        
        ## define a page with list of books
        ## BookListView is a subclass of Django's class-based generic view (i.e. ListView).  The generic view already implements many of usefll functionality
        ## .as_view() properly converts a class-based view into a view method/function
        path('books/', views.BookListView.as_view(), name='books'),
        
        ## define a page with detailed information of a book and its associated copies
        ## <int:pk> captures the value from url and specifies the data type
        ## The name 'book_detail' should match with get_absolute_url() method defined in Book model 
        path('book/<int:pk>', views.BookDetailView.as_view(), name='book_details'),
        
        ## define a page with list of authors
        path('author/', views.AuthorListView.as_view(), name='authors'),
        ## define a page with author details and list of his/her books
        path('author/<int:pk>/', views.author_detail_view, name='author_details'),
        
        ## Add a view with a list of borrowed book of the loggedin user
        path('myborrow/', views.MyBorrowListView.as_view(), name='my_borrow'),
        
        ## add a view for librarian only with a list of all borrowed books
        path('allborrow/', views.AllBorrowListView.as_view(), name='all_borrow'),
        
        ## view for librarian to renew (i.e. edit due date) of a book instance
        path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
        
        ## CreateView, UpdateView and DeleteView for Book model
        path('books/create/', views.BookCreate.as_view(), name='book_create'),
        path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
        path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
        
        ## CreateView, UpdateView, and DeleteView for Author model
        path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
        path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
        path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
        ]