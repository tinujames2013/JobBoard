from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    # Example URL patterns for the admin panel
    path('', views.home, name='admin_home'),
   
]
