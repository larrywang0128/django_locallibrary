from django.shortcuts import render

###########################
# Create your views here. #
###########################
# Import the model classes that we will use to access data in all our views
from catalog.models import Book, Author, BookInstance, Genre

# Use login_required to restrict access to logged-in users in function-based views
from django.contrib.auth.decorators import login_required
# Use LoginRequiredMixin to restrict access to logged-in users in class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
# Use PermissionRequiredMixin to restrict specific permission of users in function-based views
from django.contrib.auth.decorators import permission_required
# Use PermissionRequiredMixin to restrict specific permission of users in class-based views
from django.contrib.auth.mixins import PermissionRequiredMixin

'''
define view.index
# View function for home page of site.
'''
@login_required # If the user is logged in then your view code will execute as normal. 
                # If the user is not logged in, this will redirect to the login URL defined in the project settings (settings.LOGIN_URL), 
                # passing the current absolute path as the next URL parameter.
                # @login_required must be included for each individual view. It only works for function-based views. For class-based views, use LoginRequiredMixin
def index(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    # Count of genre values containing letter 'c'
    # __icontains is case in-sensitive
    num_genre_c = Genre.objects.filter(name__icontains='c').count()
    
    # Count the number of visit for a given user/browser by using request.session, which behaves like a dictionary
    ## get current number of visit, start with 0 if first visit
    num_visits = request.session.get('num_visits',0)
    ## increase number of visits by 1
    num_visits += 1
    ## update session data
    request.session['num_visits'] = num_visits
	
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
		 'num_genre_c': num_genre_c,
        'num_visits': num_visits,
    }
    
    # Render the HTML template index.html with the data in the context variable
    # render() generates HTML files using a template (e.g. index.html) and data (context)
    return render(request, 'index.html', context=context)

'''
define BookListView as a class-based view by referring generic class ListView
'''
from django.views import generic


class BookListView(LoginRequiredMixin, generic.ListView):
    # The generic view will query the database to get all records for the specified model (Book) 
    # then render a template located, by default, at /locallibrary/catalog/templates/catalog/book_list.html (to be created separately). 
    # Within the template you can access the list of books with the template variable named book_list
    model = Book
    
    # Change the default name (model_name_list) of the template variable. 
    context_object_name = 'list_of_books'  
    
    # Instead of listing all books (default), futher filter the list of books
#    queryset = Book.objects.filter(title__icontains='war')[:5] 
    
    # Instead of using the default html template location and name, specify a location/name
    # root folder is /locallibrary/catalog/templates/
    template_name = 'books.html'
    
    # With pagination, as soon as there are more than "paginate_by" records the view will start paginating the data it sends to the template.
    paginate_by = 4
    
    # Override get_context_data() in order to pass additional context variables to the template (e.g. the list of books is passed by default)
    def get_context_data(self, **kwargs):
        # Call the generic class first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['num_books'] = Book.objects.all().count()
        return context

'''
define BookDetailView as a class-based view from generic class DetailView
'''
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    # similar to ListView, specify model, object name (default is model name) and template location/name
    model = Book
    context_object_name = 'book'
    template_name = 'book_details.html'

'''
code below shows how BookDetailView would be defined without using generic class
'''
#def book_detail_view(request, primary_key):
#    try:
#        book = Book.objects.get(pk=primary_key)
#    except Book.DoesNotExist:
#        raise Http404('Book does not exist')
#    
#    # the two lines below have the same function as try-except above
#    ## from django.shortcuts import get_object_or_404
#    ## book = get_object_or_404(Book, pk=primary_key)
#    
#    return render(request, 'catalog/templates/book_details.html', context={'book': book})

'''
define AuthorListView
'''
class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'authors.html'
    paginate_by = 10
    
    # add count of authors in context
    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['num_authors'] = Author.objects.all().count()
        return context

'''
define author_detail_view
'''
@login_required
def author_detail_view(request, pk):
    try: 
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        raise Http404('Author does not exist')
    
    book_count = author.book_set.all().count()
    context = {'author': author, 'book_count':book_count}
    return render(request, 'author_details.html', context=context)

'''
define a list view for borrowed books of logged in user
'''
class MyBorrowListView(LoginRequiredMixin,generic.ListView):
    model=BookInstance
    context_object_name = 'myborrowedbook'
    template_name = 'my_borrow.html'
    paginate_by = 10
    
    ## Override the get_queryset() method in generic class, to change the list of records returned. 
    ## This is more flexible than just setting the queryset attribute 
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
    # add count of borrowed books in context
    def get_context_data(self, **kwargs):
        context = super(MyBorrowListView, self).get_context_data(**kwargs)
        context['num_myborrow'] = BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').count()
        return context

'''
define a list view for librarian for all borrowed books
'''
class AllBorrowListView(PermissionRequiredMixin, generic.ListView):
    ## permissions are declared under Meta class of Model
    ## Each permission is in format of app_name.permission_name. Multiple permissions can be required in a tuple
    ## permission need to be assigned to user via admin app
    permission_required = 'catalog.view_all_borrow'
    model = BookInstance
    context_object_name = 'allborrowedbook'
    template_name = 'all_borrow.html'
    ## return all borrowed books, and order by title and due date
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('book', '-due_back') # due_back is in descending order
    ## add number of borrowed books to context
    def get_context_date(self, **kwargs):
        context = super(AllBorrowListView, self).get_context_data(**kwargs)
        context['num_borrow'] = BookInstance.objects.filter(status__exact='o').count()
        return context

'''
# define a view for librarian to renew book instance
'''
import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

# import defined forms
from catalog.forms import RenewBookForm

# limit permisison
@permission_required('catalog.can_renew_book')
def renew_book_librarian(request, pk):
    ## check whether the book instance exists in database
    book_instance = get_object_or_404(BookInstance, pk=pk)
    ## If this is a POST request then process the Form data
    if request.method == 'POST':
        ## Create a form instance and populate it with data from the request (binding):
        book_renewal_form = RenewBookForm(request.POST)
        ## Check if the form is valid:
        if book_renewal_form.is_valid():
            ## process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()
            ## redirect to a new URL:
            return HttpResponseRedirect(reverse('all_borrow') )
    ## If this is a GET (or any other method) create the default form.
    else:
        # default is 3 weeks from present date or current due date, whichever is later
        proposed_renewal_date = max(book_instance.due_back, datetime.date.today()) + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    ## Return form and data
    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }
    return render(request, 'book_renew_librarian.html', context)

'''
# define views to create, edit and delete book using generic editing views
'''
# import generic form views; using these views do not require a separate form class in forms.py
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required='catalog.can_create_book'
    model = Book
    fields = '__all__'
    initial = {'language': 'en'} # set initial value in a dictionary
    # success_url can be used to specify a redirect location after completing the creation/updaate. By default these views will redirect on success to a page displaying the newly created/edited model item
    template_name = 'book_form.html'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required='catalog.can_update_book'
    model = Book
    fields = ['title', 'author', 'summary','genre']
    template_name = 'book_form.html'

class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required='catalog.can_delete_book'
    model = Book
    # reverse_lazy() is a lazily executed version of reverse(), used here because we're providing a URL to a class-based view attribute.
    success_url = reverse_lazy('books')
    template_name = 'book_confirm_delete.html'

'''
# define views to create, update and delete author records
'''
class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required='catalog.can_create_book' # use the same permisison as creating books
    model = Author
    fields = '__all__'
    template_name = 'author_form.html'
    initial = {'dod': '12/10/2018'}
    
class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_update_book' # same permission as updating books
    model = Author
    fields = '__all__'
    template_name = 'author_form.html'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_delete_book' # same permission as deleting books
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'author_confirm_delete.html'