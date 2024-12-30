# portfolio/urls.py

from django.contrib import admin
from django.urls import path, include  # Include 'include' for connecting app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio_content.urls')),  # Connects to URLs in portfolio_content/urls.py
]