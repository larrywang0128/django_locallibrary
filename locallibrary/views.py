from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


'''
define a view for a landing page with sign in and registration option
'''
def landing_view(request):
    # if user is already authenticated, redirect to catalog page
#    if request.user.is_authenticated:
#        return HttpResponseRedirect(reverse('catalog_app'))
#    else:
        return render(request, 'landing.html')

'''
define a view for user registration. Standard UserCreationForm is used.
'''
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def user_signup_view(request):
    # check POST vs GET request
    if request.method == 'POST':
        # populate data from POST
        reg_form = UserCreationForm(request.POST)
        
        #create the user and login
        if reg_form.is_valid():
            reg_form.save()
            
            # login user
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            
            # redirect to landing page
            return HttpResponseRedirect(reverse('landing'))
    # for GET request, display empty form
    else:
        reg_form = UserCreationForm()
    return render(request, 'signup.html', context={'form':reg_form})