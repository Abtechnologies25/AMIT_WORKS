from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('reject-user/<int:user_id>/', views.reject_user, name='reject_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('work-status-group/', views.work_status_group_list, name='work_status_group_list'),

    path('workstatus/', views.workstatus_branch_list, name='workstatus_branch_list'),
    path('workstatus/<str:branch>/', views.workstatus_department_list, name='workstatus_department_list'),
    path('workstatus/<str:branch>/<str:department>/', views.workstatus_records_view, name='workstatus_records_view'),
    path('work-status-group/add/', views.create_work_status_group, name='create_work_status_group'),
    path('work-status-group/<int:group_id>/edit/', views.edit_work_status_group, name='edit_work_status_group'),
    path('work-status-group/<int:group_id>/delete/', views.delete_work_status_group, name='delete_work_status_group'),

 
    path('work-status/<int:group_id>/add/', views.add_work_status, name='add_work_status'),
    path('work-status/<int:status_id>/edit/', views.edit_work_status, name='edit_work_status'),
    path('work-status/<int:status_id>/delete/', views.delete_work_status, name='delete_work_status'),
    path('work-status-group/download/', views.download_work_status_report, name='download_work_status_report'),
]