import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookForm

# test class for RenewBookForm. This test does not involve database operation
class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()        
        # we also have to test whether the label value is None, because even though Django will render the correct label. It returns None if the value is not explicitly set.
        self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'Renewal Date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 12 weeks.')
    
    # We also need to validate that the correct errors are raised if the form is invalid, however this is usually done as part of view testing.
    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=12) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
        
    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=12) 
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())