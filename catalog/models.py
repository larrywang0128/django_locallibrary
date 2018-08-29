from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
''' "Book" model represents a book (but not a specific copy)'''
class Book(models.Model):
    # Fields
    title = models.CharField(max_length=200, help_text='Enter the book title')
    
    ## ForeignKey is used because we assume there one book has no more than one author (though it is not true in reality).
    ## null=True allows NULL to be stored when author information is not provided
    ## on_delete=models.SET_NULL allows author value to be reset to NULL when associated author record is deleted.
    ## The first unnamed argument can be Author (without quotation) if Author class is already defined prior.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, help_text='Select the author name')
    
    summary = models.TextField(max_length=5000, help_text='Enter a brief book summary')
    
    ## The first unnamed argument 'ISBN' specifies the verbose name of the field.
    ## An html format link is included in the help text to show ISBN definition.
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    ## ManyToManyField is used because we assume many-to-many relationship between book and genre. 
    ## The first unnamed argument can be Genre (without quotation) if Genre class is already defined prior.
    ## The default value is blank=False, meaning every book must have a genre.
    genre = models.ManyToManyField('Genre', help_text='Select a genre for the book')
    
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    
    pubdate = models.DateField(help_text='Enter the publication date')
    
    ## auto_now_add=True sets the datetime only when the model is first created
    create_dt = models.DateTimeField(auto_now_add=True, help_text='Creation datetime of the record')
    
    # Meta
    class Meta:
        ## Sort the records by title A-Z and publication date new-old
        ordering = ['title', '-pubdate']
        permissions = (('can_create_book','Add new books'),
                       ('can_update_book','Update book details'),
                       ('can_delete_book', 'Delete books'),
                )
        
    # Methods
    def __str__(self):
        ## use book title as the representation
        return self.title
    
    def get_absolute_url(self):
        ## Returns the url to access a detail record for this book.
        ## 'book_details' is the view that display the record. It will be created separately.
        return reverse('book_details', args=[str(self.id)])
    
    def display_genre(self):
        ## Return the first 3 genre values of each book in a string 
        return ", ".join(genre.name for genre in self.genre.all()[:3])
    ## Create a short_description that can be used in the admin site 
    display_genre.short_description = 'Genre'
        
''' "Genre" model represents that category of a book'''
class Genre(models.Model):
    # Fields
    name = models.CharField(max_length = 200, help_text = 'Enter genre of the book (e.g. Science Fiction)')
    
    # Meta
    class Meta:
        ordering = ['name'] 
        
    # Methods
    def __str__(self):
        return self.name 

''' "Author" model represents the authors and their biographics '''
class Author(models.Model):
    # Fields
    first_name = models.CharField(max_length=50, help_text='Enter the frist name')
    last_name = models.CharField(max_length=50, help_text='Enter the last name')
    ## Both date of birth and date of death are allowed to be blank
    dob = models.DateField(verbose_name='Date of Birth', blank=True, null=True, help_text='Enter date of birth')
    dod = models.DateField(verbose_name='Date of Death', blank=True, null=True, help_text='Enter date of death (leave blank if still alive)')
    
    # Meta
    class Meta:
        ordering = ['last_name', 'first_name']
    
    # Methods:
    def __str__(self):
        ## use last name and first name as the representation
        return '%s, %s' % (self.last_name, self.first_name)
    
    def get_absolute_url(self):
        return reverse('author_details', args=[str(self.id)])

''' "BookInstance" model represents a specific copy of a book '''
class BookInstance(models.Model):
    # Fields:
    ## UUIDField allocates a globally unique value for each instance (one for every book you can find in the library)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    ## ForeignKey links BookInstance to Book
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, help_text='Enter version details')
    due_back = models.DateField(null=True, blank=True, help_text='Enter due date to return')
    ## ForeignKey links BookInstance to User (who borrowed a specific copy of book)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    ## define a list of status. Choice values are defined in format of a tuple containing tuples of key-value pairs. 
    ## Key is the value stored in database while either key or value can be displayed. 
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    
    # Meta
    class Meta:
        ordering = ['due_back']
        
        ## declare a permission for viewing all borrowed books
        ## Define multiple permissions in a tuple. Each permission is a tuple with (permission_name, permission_display_value)
        permissions = (('view_all_borrow', 'View all borrowed books'),
                       ('can_renew_book', 'Renew a book'),
                )
        
    # Methods
    def __str__(self):
        ## use copy id and book title as the representation
        return '%s (%s)' % (self.book.title, self.id)
    
    ## check whether the copy of book is overdue. 
    @property ### @property here defines a read-only property BookInstance.is_overdue
              ### see examples at https://docs.python.org/3/library/functions.html#property
    def is_overdue(self):
        if self.due_back and date.today()>self.due_back:
            return True
        return False

''' "Language" model represents the lanuage used by the book'''
class Language(models.Model):
    # Fields
    LANGUAGE = (
            ('en', 'English'),
            ('cn', 'Chinese'),
            ('sp', 'Spanish'),
            ('fr', 'Frech'),
    )
    name = models.CharField(max_length=2, choices=LANGUAGE, help_text='Select the language of the book')
    
    # Meta
    class Meta:
        ordering = ['name']
    
    # Methods
    def __str__(self):
        return self.name
