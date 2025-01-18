from django.urls import path
from . import views
from .views import (
    create_profile,
    edit_profile,
    view_profile,
)

app_name = 'users'

urlpatterns = [
    
    path('', views.home, name='users_home'),
    path('profile/create/', create_profile, name='create_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/view/', view_profile, name='view_profile'),
    path('profile/edit/', views.edit_candidate_profile, name='edit_candidate_profile'),
    path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('upload_documents/', views.upload_documents, name='upload_documents'),
    path('job-list/', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('my-applications/', views.application_list, name='application_list'),
    path('<int:job_id>/expired/', views.job_expired, name='job_expired'),
    path('search/', views.job_search, name='job_search'),
    path('search/results/', views.job_search_results, name='job_search_results'),
    path('application-status/', views.application_status, name='application_status'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('application/<int:id>/', views.view_application, name='view_application'),
    path('withdraw-application/<int:application_id>/', views.withdraw_application, name='withdraw_application'),
    path('notifications/', views.candidate_notifications, name='candidate_notifications'),
    path('email-preview/', views.candidate_email_preview, name='candidate_email_preview'),
    path('upload-documents/', views.upload_documents, name='upload_documents'),
    path('view-resume/', views.view_resume, name='view_resume'),
    path('profile/', views.view_profile, name='view_profile'),  # For the logged-in user's profile
    path('profile/<str:username>/', views.view_profile, name='view_profile_by_username'), # For other users' profiles
    path('logout/', views.logout_view, name='logout'),

]



    



