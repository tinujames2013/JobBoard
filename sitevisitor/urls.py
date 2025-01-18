from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    home,
    login_view,
    register_view,
    
    
   
)

app_name = 'sitevisitor'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
   path('reset_password/', 
         auth_views.PasswordResetView.as_view(), 
         name='reset_password'),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),  # This is the critical line
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
]

  

