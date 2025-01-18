from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home, name='jobs_home'),
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('post/', views.post_job, name='post_job'), 
    path('manage-jobs/', views.manage_jobs, name='manage_jobs'),
    path('job/<int:job_id>/', views.job_view, name='job_view') ,
    path('candidate-search/', views.candidate_search, name='candidate_search'),
    path('applications-dashboard/', views.applications_dashboard, name='applications_dashboard'),
    path('application-details/<int:application_id>/', views.application_details, name='application_details'),
    path('filter-applications/', views.filter_applications, name='filter_applications'),
    path('candidate-communication/', views.candidate_communication, name='candidate_communication'),
    path('recruiter-notifications/', views.recruiter_notifications, name='recruiter_notifications'),
    path('recruiter/profile/', views.recruiter_profile, name='recruiter_profile'),
    path('edit-recruiter-profile/', views.edit_recruiter_profile, name='edit_recruiter_profile'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('view-profile/', views.view_profile, name='view_profile'),
    path('list/', views.applications_list, name='applications_list'),
    path('candidate-communication/<int:application_id>/', views.candidate_communication, name='candidate_communication'),
    path('application-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('notifications/', views.my_notifications, name='my_notifications'),
    path('logout/', views.logout_view, name='logout'),
    path('job/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('job/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('job/status/<int:job_id>/', views.change_job_status, name='change_job_status'),

]
