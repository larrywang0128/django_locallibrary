from django.test import TestCase

'''
a dummy test class below to demonstrate how test works
'''
#class YourTestClass(TestCase):
#    @classmethod
#    def setUpTestData(cls):
#        print("setUpTestData: Run once to set up non-modified data for all class methods.")
#        pass
#    # setUp() will run before every test method
#    def setUp(self):
#        print("setUp: Run once for every test method to setup clean data.")
#        pass
#    # three dummy test methods are defined below
#    def test_false_is_false(self):
#        print("Method: test_false_is_false.")
#        self.assertFalse(False)
#
#    def test_false_is_true(self):
#        print("Method: test_false_is_true.")
#        self.assertTrue(False)
#
#    def test_one_plus_one_equals_two(self):
#        print("Method: test_one_plus_one_equals_two.")
#        self.assertEqual(1 + 1, 2)

# import the model to be tested
from catalog.models import Author

# use descriptive class name related to the model under test. best practice is to create one test class for each model/view/form/etc.
class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods. This object will not be changed throughout the test class.
        Author.objects.create(first_name='Big', last_name='Bob')
    
    # use descriptive name for each test method
    # test whether label of first_name (i.e. verbose_name) is 'first name'. 
    def test_first_name_label(self):
        # Get an author object to test
        author = Author.objects.get(id=1)
        # Get the metadata for the required field and use it to query the required field data
        field_label = author._meta.get_field('first_name').verbose_name
        # Compare the value to the expected result
        self.assertEquals(field_label, 'first name')

    def test_dod_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('dod').verbose_name
        self.assertEquals(field_label, 'Date of Death')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1/')