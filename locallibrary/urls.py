"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
]


# Use include() to add paths from the catalog application 
from django.conf.urls import include

urlpatterns += [
    path('catalog/', include('catalog.urls')),
]

# Add URL maps to redirect the base URL to our application
# Since catalog is the only app, we redirect the root URL of our site (i.e. 127.0.0.1:8000) to the URL 127.0.0.1:8000/catalog/
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='catalog/')),
]

# Django does not serve static files like CSS, JavaScript, and images by default.
# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Add Django site authentication urls (for login, logout, password management)
# It is better to separate authentication from an specific application
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

