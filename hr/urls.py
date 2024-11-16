from django.urls import path
from . import views

urlpatterns = [
    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employee/edit/<str:employee_id>/', views.employee_edit, name='employee_edit'),  # Changed to <str:employee_id>
    path('employee/delete/<str:employee_id>/', views.employee_delete, name='employee_delete'),
    path('employees/live_search/', views.employee_live_search, name='employee_live_search'),
    path('employees/<str:employee_id>/', views.employee_detail, name='employee_detail'),  # Changed to <str:employee_id>
    path('employees/generate_payslips/', views.generate_payslips, name='generate_payslips'),

    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),


    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.attendance_add, name='attendance_add'),
    path('attendance/edit/<int:record_id>/', views.attendance_edit, name='attendance_edit'),
    path('attendance/delete/<int:record_id>/', views.attendance_delete, name='attendance_delete'),


    # Leave URLs
    path('leaves/', views.leave_list, name='leave_list'),
    path('leaves/add/', views.leave_add, name='leave_add'),
    path('leaves/<int:leave_id>/', views.leave_detail, name='leave_detail'),  # Detail view route
    path('leaves/<int:leave_id>/edit/', views.leave_edit, name='leave_edit'),
    path('leaves/<int:leave_id>/delete/', views.leave_delete, name='leave_delete'),
    path('leaves/<int:leave_id>/approve/', views.leave_approve, name='leave_approve'),

    # Payroll URLs
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/add/', views.payroll_add, name='payroll_add'),
    path('payroll/<int:id>/edit/', views.payroll_edit, name='payroll_edit'),
    path('payroll/<int:id>/delete/', views.payroll_delete, name='payroll_delete'),

    # Deduction URLs (if you want to manage them separately)
    path('deductions/', views.deduction_list, name='deduction_list'),
    path('deductions/add/', views.deduction_add, name='deduction_add'),
    path('deductions/delete/<int:deduction_id>/', views.deduction_delete, name='deduction_delete'),

    # HR Dashboard
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),
]
