from django.contrib import admin

''' 
# Register your models here.
'''
from .models import Author, Genre, Book, BookInstance, Language

'''
# Inline classes enable editing associated records (e.g. BookInstance) at the same time of editing the main record (e.g. Book)
# There are two types of inline classes TabularInline (horizonal layout) or StackedInline (vertical layout, just like the default model layout)
'''
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    ## specific how may place holder records (i.e. blank record) to be displayed within Inline. The default is 3. Minimum is 0. 
    extra = 1
    
class BookInline(admin.StackedInline):
    model = Book
    extra = 0

'''
# create a subclass under ModelAdmin class to configure admin page for a model
'''
class AuthorAdmin(admin.ModelAdmin):
    ## On list view, display last name, first name, date of birth, date of death for Author page on admin site
    list_display = ('last_name', 'first_name', 'dob', 'dod')
    ## On form view (for add and edit), specify how fields are displayed. Fields will be displayed horizontally if included in a tuple
    fields = ['first_name', 'last_name', ('dob', 'dod')]
    inlines = [BookInline]
admin.site.register(Author, AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    ## The foreign key, author, can be directly referred here. 
    ## Unfortunately we can't directly specify the genre field in list_display 
    ## because it is a ManyToManyField (Django prevents this because there would be a large database access "cost" in doing so). 
    ## Instead we'll define a display_genre function to get the information as a string.
    ## The function is defined in Methods of Book model in model.py 
    list_display = ('title', 'author', 'display_genre')
    ## add Inline class defined above
    inlines = [BookInstanceInline]
admin.site.register(Book, BookAdmin)

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'id', 'status', 'due_back','borrower')
    ## On list view, add filter to admin site
    list_filter = ('status', 'due_back')
    ## On form view, group fields into sections. 
    ## Each section has its own title (or None, if you don't want a title) and an associated tuple of fields in a dictionary
    fieldsets = (
            ### setion 1 (without title)
            (None, {'fields':('book', 'imprint', 'id')}),
            ### section 2
            ('Availability', {'fields':('status', 'due_back','borrower')}),
            )
admin.site.register(BookInstance, BookInstanceAdmin)

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
#admin.site.register(BookInstance)
