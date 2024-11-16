from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Department, Employee, Attendance, Leave, Payroll, Deduction, Department
from .forms import DepartmentForm, AttendanceForm, LeaveForm, PayrollForm, EmployeeForm, DeductionForm
from django.core.paginator import Paginator
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Count


@login_required(login_url='/auth/login/')
@login_required(login_url='/auth/login/')
def hr_dashboard(request):
    # Total Employees
    total_employees = Employee.objects.count()

    # Employees on Leave
    employees_on_leave = Leave.objects.filter(approved=True).count()

    # Department Breakdown
    department_counts = Department.objects.annotate(num_employees=Count('employee')).values('name', 'num_employees')

    # Attendance Summary (Last 7 Days)
    recent_attendance = Attendance.objects.filter(date__gte=timezone.now() - timezone.timedelta(days=7))
    attendance_summary = (
        recent_attendance
        .values('date')
        .annotate(total=Count('id'))
        .order_by('date')
    )

    # Leave Statistics (Approved vs Pending)
    leave_approved = Leave.objects.filter(approved=True).count()
    leave_pending = Leave.objects.filter(approved=False).count()

    # Recent Payroll
    recent_payrolls = Payroll.objects.all().order_by('-date')[:5]

    context = {
        'total_employees': total_employees,
        'employees_on_leave': employees_on_leave,
        'department_counts': list(department_counts),  # Convert QuerySet to list
        'attendance_summary': list(attendance_summary),  # Convert QuerySet to list
        'leave_approved': leave_approved,
        'leave_pending': leave_pending,
        'recent_payrolls': recent_payrolls,
    }

    return render(request, 'hr/hr_dashboard.html', context)

@login_required(login_url='/auth/login/')
def employee_list(request):
    employees = Employee.objects.all().order_by('first_name')
    departments = Department.objects.all()
    form = EmployeeForm()
    return render(request, 'hr/employee_list.html', {
        'employees': employees,
        'form': form,
        'departments': departments,
    })


@login_required(login_url='/auth/login/')
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    return render(request, 'hr/employee_detail.html', {'employee': employee})


@login_required(login_url='/auth/login/')
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully.')
            return redirect('employee_list')
    return redirect('employee_list')


@login_required(login_url='/auth/login/')
def employee_edit(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'hr/employee_edit.html', {'form': form, 'employee': employee})


@login_required(login_url='/auth/login/')
def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('employee_list')


@login_required(login_url='/auth/login/')
def employee_print(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    template_path = 'hr/employee_print.html'
    context = {'employee': employee}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{employee.first_name}_{employee.last_name}_details.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error rendering PDF', status=500)
    return response


@login_required(login_url='/auth/login/')
def generate_payslips(request):
    if request.method == 'POST':
        employee_ids = request.POST.getlist('employee_ids')
        if not employee_ids:
            messages.error(request, "No employees selected.")
            return redirect('employee_list')

        employees = Employee.objects.filter(employee_id__in=employee_ids)
        payrolls = Payroll.objects.filter(employee__in=employees)

        context = {'payrolls': payrolls}

        template_path = 'hr/payslip_template.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="payslips.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error generating PDF payslips', status=500)
        return response

    return redirect('employee_list')


@login_required(login_url='/auth/login/')
def payroll_list(request):
    payrolls = Payroll.objects.all()
    paginator = Paginator(payrolls, 10)  # Show 10 payrolls per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    add_form = PayrollForm()
    edit_forms = {payroll.id: PayrollForm(instance=payroll) for payroll in payrolls}

    context = {
        'payrolls': page_obj,
        'add_form': add_form,
        'edit_forms': edit_forms,
    }
    return render(request, 'hr/payroll_list.html', context)


@login_required(login_url='/auth/login/')
@login_required(login_url='/auth/login/')
def payroll_add(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.basic_salary = payroll.employee.salary  # Ensure salary matches the employee's record
            payroll.calculate_net_salary()
            payroll.save()
            messages.success(request, "Payroll record added successfully.")
            return redirect('payroll_list')
    else:
        form = PayrollForm()

    return render(request, 'hr/payroll_add.html', {'form': form})

@login_required(login_url='/auth/login/')
def payroll_edit(request, id):
    payroll = get_object_or_404(Payroll, id=id)
    if request.method == 'POST':
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            payroll.calculate_net_salary()
            return redirect('payroll_list')
    return redirect('payroll_list')


@login_required(login_url='/auth/login/')
def payroll_delete(request, id):
    payroll = get_object_or_404(Payroll, id=id)
    payroll.delete()
    return redirect('payroll_list')


@login_required(login_url='/auth/login/')
def department_list(request):
    departments = Department.objects.all().order_by('name')
    paginator = Paginator(departments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = DepartmentForm()  # Ensure this is passed to the template

    return render(request, 'hr/department_list.html', {
        'departments': page_obj,
        'form': form,  # Ensure this is passed
    })


@login_required(login_url='/auth/login/')
def department_add(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()

    return render(request, 'hr/department_add.html', {'form': form})


@login_required(login_url='/auth/login/')
def leave_list(request):
    leaves = Leave.objects.all().order_by('-start_date')

    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave request added successfully.')
            return redirect('leave_list')
    else:
        form = LeaveForm()

    context = {
        'leaves': leaves,
        'form': form
    }

    return render(request, 'hr/leave_list.html', context)


# Leave Detail View with Edit, Delete, and Approve Modals
@login_required(login_url='/auth/login/')
def leave_detail(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)

    if request.method == 'POST':
        # Handle edit form submission
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave request updated successfully.')
            return redirect('leave_detail', leave_id=leave.id)
    else:
        form = LeaveForm(instance=leave)

    context = {
        'leave': leave,
        'form': form
    }

    return render(request, 'hr/leave_detail.html', context)


# Approve Leave
@login_required(login_url='/auth/login/')
def leave_approve(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    if request.method == 'POST':
        leave.approved = True
        leave.save()
        messages.success(request, 'Leave request approved successfully.')
        return redirect('leave_detail', leave_id=leave.id)

    context = {
        'leave': leave
    }

    return render(request, 'hr/leave_detail.html', context)


# Delete Leave
@login_required(login_url='/auth/login/')
def leave_delete(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    if request.method == 'POST':
        leave.delete()
        messages.success(request, 'Leave request deleted successfully.')
        return redirect('leave_list')

    context = {
        'leave': leave
    }

    return render(request, 'hr/leave_detail.html', context)


# Add Leave Functionality (can be triggered through a modal or a separate view)
@login_required(login_url='/auth/login/')
def leave_add(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave request added successfully.')
            return redirect('leave_list')

    else:
        form = LeaveForm()

    context = {
        'form': form
    }

    return render(request, 'hr/leave_add.html', context)


# Edit Leave (Embedded in Detail Page)
@login_required(login_url='/auth/login/')
def leave_edit(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)

    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave request updated successfully.')
            return redirect('leave_detail', leave_id=leave.id)
    else:
        form = LeaveForm(instance=leave)

    context = {
        'leave': leave,
        'form': form
    }

    return render(request, 'hr/leave_detail.html', context)

@login_required(login_url='/auth/login/')
def attendance_list(request):
    # Fetch attendance records with pagination
    attendance_records = Attendance.objects.select_related('employee').order_by('-date')
    paginator = Paginator(attendance_records, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch employees for the dropdown
    employees = Employee.objects.all().order_by('first_name', 'last_name')

    # Handle adding attendance
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        date = request.POST.get('date')
        status = request.POST.get('status')

        if not employee_id or not date or not status:
            messages.error(request, "All fields are required.")
            return redirect('attendance_list')

        # Check if the attendance record already exists
        employee = get_object_or_404(Employee, id=employee_id)
        if Attendance.objects.filter(employee=employee, date=date).exists():
            messages.error(request, f"Attendance for {employee.first_name} {employee.last_name} on {date} already exists.")
            return redirect('attendance_list')

        # Create the attendance record
        Attendance.objects.create(employee=employee, date=date, status=status)
        messages.success(request, f"Attendance for {employee.first_name} {employee.last_name} on {date} added successfully.")
        return redirect('attendance_list')

    return render(request, 'hr/attendance_list.html', {
        'attendance_records': page_obj,
        'employees': employees,
    })

@login_required(login_url='/auth/login/')
def attendance_add(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')  # Get employee ID from form
        date = request.POST.get('date')
        status = request.POST.get('status')


        # Validate and fetch employee
        try:
            employee = get_object_or_404(Employee, id=employee_id)
        except Exception:
            messages.error(request, "Selected employee does not exist.")
            return HttpResponseRedirect(reverse('attendance_list'))

        # Prevent duplicate attendance record
        if Attendance.objects.filter(employee=employee, date=date).exists():
            messages.error(request, f"Attendance for {employee.first_name} {employee.last_name} on {date} already exists.")
            return HttpResponseRedirect(reverse('attendance_list'))

        # Save attendance record
        Attendance.objects.create(employee=employee, date=date, status=status)
        messages.success(request, f"Attendance for {employee.first_name} {employee.last_name} on {date} added successfully.")
        return HttpResponseRedirect(reverse('attendance_list'))

    return render(request, 'hr/attendance_add.html')

@login_required(login_url='/auth/login/')
def attendance_edit(request, record_id):
    attendance_record = get_object_or_404(Attendance, id=record_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        status = request.POST.get('status')

        if not date or not status:
            messages.error(request, "Date and status are required.")
            return redirect('attendance_list')

        attendance_record.date = date
        attendance_record.status = status
        attendance_record.save()

        messages.success(request, "Attendance record updated successfully.")
        return redirect('attendance_list')

    return render(request, 'hr/attendance_edit.html', {'record': attendance_record})


@login_required(login_url='/auth/login/')
def attendance_delete(request, record_id):
    attendance_record = get_object_or_404(Attendance, id=record_id)
    if request.method == 'POST':
        attendance_record.delete()
        messages.success(request, "Attendance record deleted successfully.")
    return redirect('attendance_list')

# List all deductions
@login_required(login_url='/auth/login/')
def deduction_list(request):
    deductions = Deduction.objects.all().order_by('-date')

    form = DeductionForm()  # The form will allow adding a new deduction
    context = {
        'deductions': deductions,
        'form': form,
    }

    return render(request, 'hr/deduction_list.html', context)

# Add a new deduction via modal
@login_required(login_url='/auth/login/')
def deduction_add(request):
    if request.method == 'POST':
        form = DeductionForm(request.POST)
        employees = Employee.objects.all()

        if form.is_valid():
            form.save()
            messages.success(request, 'Deduction added successfully.')
            return redirect('deduction_list')
    return redirect('deduction_list')

# Delete a deduction via modal
@login_required(login_url='/auth/login/')
def deduction_delete(request, deduction_id):
    deduction = get_object_or_404(Deduction, id=deduction_id)
    if request.method == 'POST':
        deduction.delete()
        messages.success(request, 'Deduction deleted successfully.')
        return redirect('deduction_list')

    return render(request, 'hr/deduction_list.html', {'deduction': deduction})


@login_required(login_url='/auth/login/')
def employee_live_search(request):
    query = request.GET.get('q', '').strip()
    employees = Employee.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )
    results = [{'id': emp.id, 'name': f"{emp.first_name} {emp.last_name}"} for emp in employees]
    return JsonResponse(results, safe=False)