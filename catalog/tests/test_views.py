from django.test import TestCase
from django.urls import reverse

from catalog.models import Author
from django.contrib.auth.models import User # Required to assign User as a borrower
'''
# test class for AuthorListView
'''
class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}',
            )
        # create a test user and login, because AuthorListView require user authentication. Without ti, response will be redirected to 'accounts/login/?next=/catalog/author/'
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()
    def setUp(self):
        login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        
    # response status code 200 indicates success.
    # user client subclass to simulate a get request for the view        
    def test_view_url_exists_at_desired_location(self): 
        # response is the output rendered by the view
        response = self.client.get('/catalog/author/') 
        self.assertEqual(response.status_code, 200)  
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
    
    # this tests the template_name 
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authors.html')
        
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        # response.context is context variable passed to the template by the view
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 3)


import datetime

from django.utils import timezone

from catalog.models import BookInstance, Book, Genre, Language
'''
# test class for MyBorrowListView
'''
class MyBorrowListViewTest(TestCase):
    # setup the database with 2 users, 1 book, and 30 copies. Assign copies equally to users
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK') 
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()
        
        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='en')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
            language=test_language,
            pubdate = datetime.date.today()
        )

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.now() + datetime.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            BookInstance.objects.create(
                book=test_book,
                imprint='Unlikely Imprint, 2016',
                due_back=return_date, 
                borrower=the_borrower,
                status=status,
            )
        
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my_borrow'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/myborrow/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my_borrow'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'my_borrow.html')
    
    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my_borrow'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        
        # Check that initially we don't have any books in list (none on loan)
        self.assertTrue('myborrowedbook' in response.context)
        self.assertEqual(len(response.context['myborrowedbook']), 0)
        
        # Now change 10 books to be on loan 
        books = BookInstance.objects.all()[:10]

        for book in books:
            book.status = 'o'
            book.save()
        
        # Check that now we have borrowed books in the list
        response = self.client.get(reverse('my_borrow'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue('myborrowedbook' in response.context)
        
        # Confirm all books belong to testuser1 and are on loan
        for bookitem in response.context['myborrowedbook']:
            self.assertEqual(response.context['user'], bookitem.borrower)
            self.assertEqual('o', bookitem.status)

    def test_pages_ordered_by_due_date(self):
        # Change all books to be on loan
        for book in BookInstance.objects.all():
            book.status='o'
            book.save()
            
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my_borrow'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
                
        # Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual(len(response.context['myborrowedbook']), 10)
        
        last_date = 0
        for book in response.context['myborrowedbook']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back

'''
# test class for renew_book_librarian
'''
import uuid

from django.contrib.auth.models import Permission # Required to grant the permission needed to set a book as returned.

class RenewBookLibrarianTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        # assign permission to user2
        permission = Permission.objects.get(name='Renew a book')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='en')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
            language=test_language,
            pubdate = datetime.date.today()
        )
        
        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user1,
            status='o',
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user2,
            status='o',
        )
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))
        
        # Check that it lets us login - this is our book and we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        
        # Check that it lets us login. We're a librarian, so we can view any users book
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk':test_uid}))
        self.assertEqual(response.status_code, 404)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'book_renew_librarian.html')
    
    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)
        # response.context['form'].initial['renewal_date'] gives the initial value ofr renewal_date
        date_3_weeks_in_future = max(self.test_bookinstance1.due_back, datetime.date.today()) + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['renewal_date'], date_3_weeks_in_future)
    
    def test_redirects_to_all_borrowed_book_list_on_success(self):
        # make sure testuser2 has permission 'View all borrowed books', otherwise, response will be redirected to '/accounts/login/?next=/catalog/allborrow/'
        test_user2 = User.objects.get(username='testuser2')
        permission = Permission.objects.get(name='View all borrowed books')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        # use client.post to simulate a POST request with data (as the second argument) 
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':valid_date_in_future})

        self.assertRedirects(response, reverse('all_borrow'))
    
    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')       
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': date_in_past})
        self.assertEqual(response.status_code, 200)
        # test form error and associated error message
        self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal in past')
        
    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=20)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': invalid_date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal more than 12 weeks ahead')

'''
Define test class for AuthorCreate view
'''
class AuthorCreateTest(TestCase):
    # setup the user model with permission
    @classmethod
    def setUpTestData(cls):
        # create two users
        testuser1 = User.objects.create_user(username='user1', password='1p2o3i4u')
        testuser1.save()
        testuser2 = User.objects.create_user(username='user2', password='p1o2i3u4')
        testuser2.save()
        
        # assign user2 with can_create_book permission
        permission = Permission.objects.get(name='Add new books')
        testuser2.user_permissions.add(permission)
        testuser2.save()
    
    # initial value of date of death is 12/10/2018
    def test_initial_date_of_death(self):
        login = self.client.login(username='user2', password='p1o2i3u4')
        response = self.client.get(reverse('author_create'))
        # self.assertRedirects(response,'/account/login')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['dod'], '12/10/2018')
    
    # user permission is can_create_book
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author_create'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/author/create/')
    
    def test_forbidden_if_logged_in_without_permission(self):
        login = self.client.login(username='user1', password='1p2o3i4u')
        response = self.client.get(reverse('author_create'))
        self.assertEqual(response.status_code, 403)
    
    def test_success_if_logged_in_with_permission(self):
        login = self.client.login(username='user2', password='p1o2i3u4')
        response = self.client.get(reverse('author_create'))
        self.assertEqual(response.status_code, 200)
        
    # template name is 'author_form.html'
    def test_template_name(self):
        login = self.client.login(username='user2', password='p1o2i3u4')
        response = self.client.get(reverse('author_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author_form.html')