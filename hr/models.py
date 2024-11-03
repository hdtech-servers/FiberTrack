from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    # Personal Information
    employee_id = models.CharField(max_length=10, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, unique=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)

    # Employment Information
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    # Bank Details
    bank = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)

    # Document Uploads
    profile_photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    id_scan_front = models.ImageField(upload_to='id_scans/', null=True, blank=True)
    id_scan_back = models.ImageField(upload_to='id_scans/', null=True, blank=True)
    additional_documents = models.FileField(upload_to='employee_documents/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate employee ID if it's a new employee
        if not self.employee_id:
            max_id = Employee.objects.aggregate(max_id=models.Max('id'))['max_id']
            new_id = max_id + 1 if max_id else 1
            self.employee_id = f'HKL{new_id:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')))

    class Meta:
        unique_together = ('employee', 'date')  # Ensure one attendance record per employee per day

    def clean(self):
        # Ensure an attendance record can't be duplicated for the same employee on the same day
        if Attendance.objects.filter(employee=self.employee, date=self.date).exists():
            raise ValidationError(f"Attendance for {self.employee} on {self.date} has already been recorded.")

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.date} - {self.status}"


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.start_date} to {self.end_date}"


class Deduction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='deductions')
    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)  # Add this field to track the date of the deduction

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.reason}"


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    date = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.ManyToManyField(Deduction, blank=True, related_name='payrolls')
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def calculate_net_salary(self):
        # Sum all deduction amounts linked to this payroll
        total_deductions = sum(deduction.amount for deduction in self.deductions.all())
        self.net_salary = self.basic_salary + self.bonus - total_deductions
        return self.net_salary

    def save(self, *args, **kwargs):
        # Calculate the net salary before saving
        self.net_salary = self.calculate_net_salary()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payroll for {self.employee.first_name} {self.employee.last_name} on {self.date}"

    class Meta:
        unique_together = ('employee', 'date')  # Ensures that there's only one payroll per employee per date
