# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 11:17:40 2018

@author: haiwa
"""

import datetime

from django import forms
from django.core.exceptions import ValidationError
# ugettext_lazy() is Django's translation function. It is a good practice if you want to translate your site later.
from django.utils.translation import ugettext_lazy as _

# create a Django form with a renewal_date field
class RenewBookForm(forms.Form):
    ## the default label (displayed in HTML) is Renewal Date
    ## a default label suffix (colon) is appended in HTML (i.e. Renewal Date:)
    renewal_date = forms.DateField(help_text="Enter a date between now and 12 weeks (default 3).")
    ## for more definitions about fields and arguments, see here: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
    
    ## Validate a single field data using clean_fieldname()
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        #E Check if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #E Check if a date is in the allowed range (+12 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=12):
            raise ValidationError(_('Invalid date - renewal more than 12 weeks ahead'))

        #E Remember to always return the cleaned data.
        return data

## A equivalent way of defining RenewBookForm() can by achieved by ModelForm. ModelForm is a convenient way to define a form from a single model.
#from django.forms import ModelForm
## import relevant model
#from catalog.models import BookInstance
#
#class RenewBookForm(ModelForm):
#    # use Meta class to define form fields based on model fields
#    class Meta:
#        model = BookInstance
#        fields = ['due_back'] # a list of field from the model
#        # Use fields = '__all__' to include all fields from the model
#        # Use exclude =['fieldname1', fieldname2'] (instead of fields) to exclude fields from the model
#        
#        # Field definitions (labels, help_texts, widgets, error_messages, etc) are inherited from the model, but can be over-written
#        labels = {'due_back':_('Renewal date')} # re-label due_back to Renewal date
#        help_texts = {'due_back':_('Enter a date between now and 12 weeks (default 3).')} # override help texts
#    
#    # To validate the field value, exact same code is used. Be aware the field name is now the same as defined in model (i.e. due_back)
#    def clean_due_back(self):
#        data = self.cleaned_data['due_back']
#        ### validation functions and errors (as above) ###
#        return data
