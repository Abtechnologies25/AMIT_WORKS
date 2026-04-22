from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('nagercoil-admin-dashboard/', views.nagercoil_admin_dashboard, name='nagercoil_admin_dashboard'),
      path('billwise-admin-dashboard/', views.billwise_admin_dashboard, name='billwise_admin_dashboard'),
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


    path('payment-voucher/<str:branch>/', views.payment_voucher_report, name='payment_voucher_report'),
    path('payment-voucher/add/<str:branch>/', views.add_payment_voucher, name='add_payment_voucher'),
    path('payment-voucher/<str:branch>/edit/<int:record_id>/', views.edit_payment_voucher, name='edit_payment_voucher'),
    path('payment-voucher/<str:branch>/delete/<int:record_id>/', views.delete_payment_voucher, name='delete_payment_voucher'),
    path('payment-voucher/download/<str:branch>/', views.download_payment_voucher_report, name='download_payment_voucher_report'),


    path('<str:branch>/registration/', views.registration_work, name='registration_work'),
    path('<str:branch>/dashboard/billwise/', views.select_work_type, name='select_work_type'),

    path('product-registration/<str:branch>/', views.product_registration_report, name='product_registration_report'),
    
   
    path('product-registration/add/<str:branch>/', views.add_product_registration, name='add_product_registration'),
    
    
    path('product-registration/<str:branch>/edit/<int:record_id>/', views.edit_product_registration, name='edit_product_registration'),
    
    
    path('product-registration/<str:branch>/delete/<int:record_id>/', views.delete_product_registration, name='delete_product_registration'),

    path('internship-registration/<str:branch>/', views.internship_registration_report, name='internship_registration_report'),
    path('internship-registration/add/<str:branch>/', views.add_internship_registration, name='add_internship_registration'),
    path('internship-registration/<str:branch>/edit/<int:record_id>/', views.edit_internship_registration, name='edit_internship_registration'),
    path('internship-registration/<str:branch>/delete/<int:record_id>/', views.delete_internship_registration, name='delete_internship_registration'),

    path('product-registration/download/<str:branch>/', views.download_product_report, name='download_product_report'),
    path('internship-registration/download/<str:branch>/', views.download_internship_report, name='download_internship_report'),

    path('<str:branch>/dashboard/<str:work_type>/', views.billwise_dashboard, name='billwise_dashboard'),
    path('<str:branch>/bill-list/<str:bill_type>/', views.bill_list, name='bill_list'),
    
    path('billwise-payment/<str:branch>/<str:bill_type>/', views.bill_list, name='bill_list'),
    path('billwise-payment/<str:branch>/<str:bill_type>/add/', views.add_bill, name='add_bill'),
    path('billwise-payment/<str:branch>/<str:bill_type>/edit/<int:record_id>/', views.edit_bill, name='edit_bill'),
    path('billwise-payment/<str:branch>/<str:bill_type>/delete/<int:record_id>/', views.delete_bill, name='delete_bill'),
    path(
    'billwise-payment/<str:branch>/<str:bill_type>/export/',
    views.export_bills_to_excel,
    name='export_bills_to_excel'
),
    path('tax-invoice/<str:branch>/', views.tax_invoice_list, name='tax_invoice_list'),
    path('tax-invoice/add/<str:branch>/', views.add_tax_invoice, name='add_tax_invoice'),
    path('tax-invoice/edit/<str:branch>/<int:invoice_id>/', views.edit_tax_invoice, name='edit_tax_invoice'),
    path('tax-invoice/delete/<str:branch>/<int:invoice_id>/', views.delete_tax_invoice, name='delete_tax_invoice'),
    path('tax-invoice/view/<str:branch>/<int:invoice_id>/', views.view_tax_invoice, name='view_tax_invoice'),
    path('tax-invoice/download/<str:branch>/<int:invoice_id>/', views.download_tax_invoice_word, name='download_tax_invoice_word'),

   path('components/<str:branch>/download/', views.download_component_stock_report, name='download_component_stock_report'),
    path('components/<str:branch>/update/<str:action>/', views.update_component_stock, name='update_component_stock'),
    path('components/<str:branch>/', views.component_list, name='component_list'),
    path('components/<str:branch>/add/', views.add_component, name='add_component'),
    path('components/<str:branch>/edit/<int:pk>/', views.edit_component, name='edit_component'),
    path('components/<str:branch>/delete/<int:pk>/', views.delete_component, name='delete_component'),
    path('admin-dashboard/components/', views.admin_component_list, name='admin_component_list'),
    path('admin-dashboard/components/add/', views.admin_add_component, name='admin_add_component'),
    path('admin-dashboard/components/edit/<str:code>/', views.admin_edit_component, name='admin_edit_component'),
    path('admin-dashboard/components/delete/<str:code>/', views.admin_delete_component, name='admin_delete_component'),
    path('admin-dashboard/components/download/', views.download_admin_component_stock_report, name='download_admin_component_stock_report'),
    path('admin-dashboard/components/history/', views.admin_component_history, name='admin_component_history'),
    path('admin-dashboard/components/history/export/', views.admin_component_history_export, name='admin_component_history_export'),

]