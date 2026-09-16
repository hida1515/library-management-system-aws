# Library Management System

A web-based **Library Management System** built with **Python**, **Django**, **MySQL**, and **Bootstrap 5**, prepared for deployment on **AWS EC2** and **AWS RDS** using **Nginx** and **Gunicorn**.

---

## 1. Project Overview

The **Library Management System** is a lightweight, responsive web application designed to digitize and automate core library operations. It enables librarians and staff to manage book inventories, track registered library patrons (members), issue books, and manage return records with automatic availability tracking and overdue calculation.

---

## 2. Problem Statement

Traditional manual library record-keeping relies on paper logs, ledger books, or fragmented spreadsheets. This approach suffers from critical operational flaws:
* **Human Error**: Miscalculated return due dates and lost physical catalog cards.
* **Lack of Real-Time Stock Tracking**: Difficulty in identifying whether a book is currently on shelves or checked out.
* **Loss of Overdue Visibility**: Inability to quickly filter which members hold overdue books.
* **Scalability Bottlenecks**: High administrative effort required to search records as the catalog grows.

The automated Library Management System addresses these issues by enforcing real-time transactional stock checks, centralizing records in a relational MySQL database, and providing a clean web dashboard.

---

## 3. Objectives

* Develop a stable Django web application following standard Model-View-Template (MVT) architecture.
* Implement full CRUD (Create, Read, Update, Delete) functionality for Books and Members.
* Build an automated Borrowing & Return engine that updates inventory (`available_quantity`) transactionally.
* Prevent invalid transactions (such as issuing out-of-stock books).
* Structure the application with environment variables (`.env`) for seamless transition between local SQLite/MySQL and cloud-hosted **AWS RDS MySQL**.
* Provide detailed academic deployment documentation for AWS EC2, Nginx, Gunicorn, and Security Groups.

---

## 4. Features

### 1. Dashboard & Analytics
* **Total Books Count**: Aggregate total copy count in the library.
* **Available Stock Count**: Real-time count of books currently on shelves.
* **Active Borrowed Count**: Total number of books currently checked out.
* **Total Members**: Total registered patrons.
* **Recent Activity Feed**: Quick tabular view of recent borrowing transactions.

### 2. Book Management (CRUD)
* Add, view list, search (title, author, ISBN, publisher), filter by category, edit, and delete books.
* Automatic tracking of `quantity` vs `available_quantity`.
* Visual stock availability badges (*Available* vs *Out of Stock*).

### 3. Member Management (CRUD)
* Register, view list, search (name, email, membership ID, phone), edit, and delete member profiles.
* Member detail view showing active borrowed items and past borrowing history.

### 4. Borrowing & Return Management
* **Issue Book**: Select available book title, member, and due date. Decrements `available_quantity` by 1.
* **Validation**: Automatically blocks issuing books when `available_quantity == 0`.
* **Return Book**: Marks record as returned, updates return date, and increments `available_quantity` by 1.
* **Overdue Tracking**: Automatically flags overdue items where `due_date < current_date`.

---

## 5. Technologies Used

* **Backend**: Python 3.9+, Django 4.2 LTS
* **Database**: MySQL 8.0 / AWS RDS MySQL (with PyMySQL driver & SQLite dev fallback)
* **Frontend**: HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons
* **Application Server**: Gunicorn (Green Unicorn)
* **Reverse Proxy / Web Server**: Nginx
* **Cloud Infrastructure**: AWS EC2 (Amazon Linux 2023 / Ubuntu), AWS RDS MySQL
* **Version Control**: Git, GitHub

---

## 6. System Architecture

```text
+------------------+
|   Client Browser |
+--------+---------+
         |
         | HTTP (Port 80)
         v
+------------------+
|   Nginx Server   | (Reverse Proxy & Static Files)
+--------+---------+
         |
         | UNIX Socket / HTTP (Port 8000)
         v
+------------------+
| Gunicorn WSGI    | (Django Application Server)
+--------+---------+
         |
         v
+------------------+
|  Django Backend  | (MVT Business Logic & Validations)
+--------+---------+
         |
         | SQL (Port 3306)
         v
+------------------+
| AWS RDS MySQL    | (Relational Database)
+------------------+
```

---

## 7. Database Design

### 1. `Book` Entity
* `id`: Primary Key (AutoField)
* `title`: CharField(200)
* `author`: CharField(150)
* `isbn`: CharField(20, unique=True)
* `category`: CharField(100)
* `publisher`: CharField(150)
* `publication_year`: IntegerField
* `quantity`: PositiveIntegerField
* `available_quantity`: PositiveIntegerField
* `created_at`: DateTimeField(auto_now_add=True)

### 2. `Member` Entity
* `id`: Primary Key (AutoField)
* `name`: CharField(150)
* `email`: EmailField(unique=True)
* `phone`: CharField(20)
* `membership_id`: CharField(50, unique=True)
* `address`: TextField(blank=True)
* `joined_date`: DateField
* `created_at`: DateTimeField(auto_now_add=True)

### 3. `Borrowing` Entity (Junction / Transaction Table)
* `id`: Primary Key (AutoField)
* `book`: ForeignKey -> `Book` (on_delete=CASCADE)
* `member`: ForeignKey -> `Member` (on_delete=CASCADE)
* `issue_date`: DateField(default=now)
* `due_date`: DateField
* `return_date`: DateField(null=True, blank=True)
* `status`: CharField(choices=['borrowed', 'returned', 'overdue'])
* `created_at`: DateTimeField(auto_now_add=True)

---

## 8. Project Structure

```text
library-management-system/
│
├── manage.py
├── requirements.txt
├── README.md
├── AWS_CHECKLIST.md
├── DEPLOYMENT_STEPS.md
├── .gitignore
├── .env.example
│
├── library_management/
│   ├── __init__.py          # PyMySQL initialization
│   ├── settings.py          # App configuration & DB setup
│   ├── urls.py              # Root routing
│   ├── wsgi.py              # WSGI entry point for Gunicorn
│   └── asgi.py
│
├── library/
│   ├── migrations/          # Database migration files
│   ├── management/
│   │   └── commands/
│   │       └── populate_library.py  # Sample data generator
│   ├── templates/
│   │   └── library/         # HTML MVT Templates
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── book_list.html
│   │       ├── book_detail.html
│   │       ├── book_form.html
│   │       ├── book_confirm_delete.html
│   │       ├── member_list.html
│   │       ├── member_detail.html
│   │       ├── member_form.html
│   │       ├── member_confirm_delete.html
│   │       ├── borrowing_list.html
│   │       └── borrowing_form.html
│   ├── static/
│   │   └── library/
│   │       └── css/
│   │           └── style.css
│   ├── __init__.py
│   ├── admin.py             # Custom Django Admin registrations
│   ├── apps.py
│   ├── forms.py             # Django ModelForms with Bootstrap
│   ├── models.py            # Book, Member, Borrowing models
│   ├── urls.py              # Application routes
│   └── views.py             # Business logic & CRUD handlers
│
└── screenshots/
    └── README.md            # Execution screenshot instructions
```

---

## 9. Prerequisites

* **Python**: Version 3.9 or higher
* **Git**: Installed locally
* **MySQL Server**: (Optional locally; SQLite is default fallback unless `.env` is populated)
* **AWS Account**: Active AWS account with EC2 and RDS access (for cloud deployment)

---

## 10. Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/library-management-system-aws.git
   cd library-management-system-aws
   ```

2. **Create and activate a virtual environment**:
   * Windows:
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   * Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 11. Virtual Environment

Always work inside the activated virtual environment to prevent package version conflicts with system-level Python.

---

## 12. MySQL Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Configure `.env` parameters for local MySQL or AWS RDS MySQL:
   ```env
   SECRET_KEY=your_custom_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=library_db
   DB_USER=admin
   DB_PASSWORD=your_mysql_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

*Note: If `DB_NAME` or `DB_HOST` is left unconfigured, the application automatically defaults to local SQLite (`db.sqlite3`), making development effortless.*

---

## 13. Migrations

Apply Django migrations to set up database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 14. Create Admin User

Create a superuser to access the Django Administration panel at `/admin/`:
```bash
python manage.py createsuperuser
```

---

## 15. Run Application

1. **Seed Fictional Sample Data** (Optional but recommended):
   ```bash
   python manage.py populate_library
   ```
2. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```
3. Open your browser and navigate to: `http://127.0.0.1:8000/`

---

## 16. CRUD Operations Overview

| Entity | Action | URL Route | Description |
| :--- | :--- | :--- | :--- |
| **Dashboard** | READ | `/` | System metrics, counts, and recent activity |
| **Book** | READ | `/books/` | List all books, search, and filter by category |
| **Book** | CREATE | `/books/add/` | Add a new book to inventory |
| **Book** | READ | `/books/<id>/` | View book metadata & borrowing history |
| **Book** | UPDATE | `/books/<id>/edit/` | Edit book details & stock quantities |
| **Book** | DELETE | `/books/<id>/delete/` | Delete book record |
| **Member** | READ | `/members/` | Directory of library members |
| **Member** | CREATE | `/members/add/` | Register a new member |
| **Member** | READ | `/members/<id>/` | View member details & active borrowings |
| **Member** | UPDATE | `/members/<id>/edit/` | Edit member profile |
| **Member** | DELETE | `/members/<id>/delete/` | Delete member record |
| **Borrowing** | READ | `/borrowings/` | View all active/returned borrowings |
| **Borrowing** | CREATE | `/borrowings/issue/` | Issue book (decrements stock) |
| **Borrowing** | UPDATE | `/borrowings/<id>/return/` | Mark returned (increments stock) |

---

## 17. AWS Deployment Overview

Deploying to AWS EC2 involves:
1. Provisioning an Amazon EC2 instance (Amazon Linux 2023 / Ubuntu).
2. Configuring Security Groups to allow Port 22 (SSH) and Port 80 (HTTP).
3. Cloning the repository to EC2.
4. Setting up Gunicorn as the WSGI HTTP application server.
5. Setting up Nginx as the frontend reverse proxy server to forward traffic from Port 80 to Gunicorn (Port 8000).

*(Refer to `DEPLOYMENT_STEPS.md` for exact execution instructions).*

---

## 18. AWS RDS Integration

1. Provision an AWS RDS MySQL instance in the same VPC as your EC2 server.
2. Configure the RDS Security Group to accept inbound traffic on Port 3306 **only** from the EC2 Security Group.
3. Update `.env` on EC2 with the RDS Endpoint address:
   ```env
   DB_HOST=library-db-instance.xxxxxx.us-east-1.rds.amazonaws.com
   ```
4. Run `python manage.py migrate` on EC2 to create tables directly on RDS MySQL.

---

## 19. Nginx Configuration

Nginx handles incoming client requests on HTTP Port 80 and serves static files directly while proxying dynamic requests to Gunicorn.
* Starts via: `sudo systemctl start nginx`
* Enables on boot: `sudo systemctl enable nginx`
* Status check: `sudo systemctl status nginx`

---

## 20. Gunicorn Configuration

Gunicorn runs Django code in multiple worker processes.
* Command: `gunicorn --bind 0.0.0.0:8000 library_management.wsgi:application`
* Managed via systemd service: `/etc/systemd/system/gunicorn.service`.

---

## 21. Security Best Practices

* **Environment Variables**: Sensitive credentials (`SECRET_KEY`, `DB_PASSWORD`) are kept inside `.env` which is excluded via `.gitignore`.
* **AWS Security Groups**: Restrict MySQL Port 3306 to EC2 Security Group ID rather than `0.0.0.0/0`.
* **SSH Key Security**: Protect `.pem` files using `chmod 400 key.pem`.
* **Least Privilege**: Grant IAM users and RDS users only required permissions.
* **Production Debug Flag**: Set `DEBUG=False` in production deployment.

---

## 22. GitHub Workflow Commands

To push this repository to GitHub:
```bash
git init
git add .
git commit -m "Initial commit - Library Management System AWS submission"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/library-management-system-aws.git
git push -u origin main
```

---

## 23. AWS Assignment Checklist Reference

Detailed fulfillment of all AWS assignment requirements (EC2, SCP, Linux Commands, Apache/Nginx, Django, React/Vite, RDS, S3, Lambda, IAM, Security Groups) is documented in [`AWS_CHECKLIST.md`](AWS_CHECKLIST.md).

---

## 24. Future Enhancements

* **Email Overdue Reminders**: Automated background task sending emails to members holding overdue books.
* **Barcode / ISBN Scanner**: Quick camera integration for book checkout.
* **Digital Media Assets**: Support for PDF previewing and e-book downloads.

---

## 25. Academic Conclusion

The **Library Management System** demonstrates the practical application of modern software engineering principles, combining Django's robust web framework with relational database management in MySQL and cloud hosting on AWS EC2 & RDS. The application fulfills all academic assignment requirements with clean architecture, strict database constraints, and production-ready deployment configurations.
