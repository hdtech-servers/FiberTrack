from django import forms

from .models import Employee, Leave, Attendance, Payroll, Department, Deduction


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address', 'national_id',
            'emergency_contact_name', 'emergency_contact_phone',
            'department', 'job_title', 'hire_date', 'salary', 'is_active',
            'bank', 'branch', 'account_number', 'profile_photo', 'id_scan_front',
            'id_scan_back', 'additional_documents'
        ]

        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_scan_front': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_scan_back': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_documents': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'start_date', 'end_date', 'reason']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control rounded-pill'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control rounded-pill', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control rounded-pill', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control rounded', 'rows': 3}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status']


class PayrollForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Payroll
        fields = ['employee', 'date', 'basic_salary', 'bonus', 'deductions']

        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'deductions': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ['employee','reason', 'amount']
