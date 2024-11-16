# FiberTrack

FiberTrack is a comprehensive Django-based ISP management system designed for integration with Mikrotik Radius, Daraja API (M-Pesa) for payments (C2B, B2C, B2B), and HR with payroll calculations. This project aims to provide Internet Service Providers (ISPs) an all-in-one tool for managing customer accounts, payments, inventory, human resources, and more.

## Features

- **ISP Management**
  - Integration with Mikrotik Radius for managing users and services.
  - Customer account management, including subscription and billing details.

- **Payment Integration**
  - Daraja API for M-Pesa payments.
    - **C2B**: Customer to Business payments for bill settlement.
    - **B2C**: Business to Customer payments for refunds.
    - **B2B**: Business to Business payments for vendor transactions.

- **Human Resource Management**
  - Employee management with payroll calculation capabilities.
  - Attendance, leave management, and payroll deductions.

- **Inventory and Services Management**
  - Inventory tracking and supplier management.
  - Service management and provisioning.

## Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/hdtech-servers/FiberTrack.git
   cd FiberTrack
   python -m venv venv
    source venv/bin/activate 
    #On Windows use `venv\Scripts\activate`

   ```

2. **Install dependencies**
   Ensure you have Python 3.8+ installed, then run:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up the Database**
   By default, the project uses SQLite. You can configure another database in the settings.
   ```sh
   python manage.py migrate
   ```

4. **Create Superuser**
   Create a superuser to access the admin panel:
   ```sh
   python manage.py createsuperuser
   ```

5. **Run the Server**
   Start the development server:
   ```sh
   python manage.py runserver
   ```

## Configuration for Production

For a production environment, additional configurations are necessary to ensure security and performance.

1. **Environment Variables**
   - **SECRET_KEY**: Replace the development secret key with a secure key stored in environment variables.
   - **DEBUG**: Set `DEBUG = False` for production.
   - **ALLOWED_HOSTS**: Specify the domain name(s) for your application.

2. **Database Configuration**
   Configure a robust database like PostgreSQL for production. Update `DATABASES` in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'fibertrack_db',
           'USER': 'fibertrack_user',
           'PASSWORD': 'secure_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Static Files**
   - Run `collectstatic` to gather all static files:
     ```sh
     python manage.py collectstatic
     ```
   - Use a web server like **Nginx** to serve static files.

4. **WSGI Server**
   Use a production-ready server such as **gunicorn**:
   ```sh
   gunicorn FiberTrack.wsgi:application --bind 0.0.0.0:8000
   ```

5. **Security Settings**
   - **HTTPS**: Configure HTTPS using **Let's Encrypt** or another SSL certificate provider.
   - **CSRF and Security Middleware**: Ensure CSRF and other security middleware are properly configured.
   - **Allowed Hosts**: Set allowed hosts to prevent HTTP Host header attacks.

6. **Celery and Redis**
   The project uses **Celery** for background tasks, with **Redis** as the broker:
   - Start Redis server:
     ```sh
     redis-server
     ```
   - Start Celery worker:
     ```sh
     celery -A FiberTrack worker --loglevel=info
     ```

## Usage

- **Admin Panel**: Accessible at `/admin/`. Use your superuser credentials to log in.
- **Customer Management**: Add, view, and edit customers and their subscription details.
- **Payments**: Manage customer payments via Daraja (M-Pesa).
- **HR and Payroll**: Manage employees, attendance, and payroll.

## Directory Structure

- **FiberTrack/**: Core project files.
- **customers/**: Customer-related models, views, and templates.
- **billing/**: Handles invoices, payments, and billing logic.
- **hr/**: Employee management and payroll.
- **static/**: Static files (CSS, JavaScript, Images).
- **templates/**: HTML templates for rendering views.

## Requirements

- **Python 3.8+**
- **Django 5.1.2**
- **Redis** for Celery
- **PostgreSQL** (recommended for production)

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For any inquiries or support, contact [support@hdtech-servers.com](mailto:support@hdtech-servers.com).

---

Feel free to explore and modify the project to suit your needs. Contributions to enhance the functionality and features of FiberTrack are always appreciated!

