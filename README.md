# 🕵️‍♂️ Crime Reporting System

A secure and user-friendly web application for reporting and managing crime cases, developed with **Django**. It allows users to submit crime reports, track their progress, and allows administrators or law enforcement officers to manage reported cases efficiently.

## 📌 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Features

### 👥 User Accounts
- User Registration and Login
- Role-based access (e.g., Admin, Officer, Citizen)
- Profile management

### 📄 Crime Reporting
- Submit a new crime report with details
- Attach evidence (images/files)
- Track the status of a report (e.g., pending, investigating, resolved)

### 📊 Admin/Officer Dashboard
- View all submitted reports
- Filter by location, category, or status
- Update report statuses and assign officers

### 🔐 Security
- Password hashing & login protection
- CSRF protection via Django
- Input validation

---

## 🛠️ Tech Stack

| Category         | Tools Used                          |
|------------------|--------------------------------------|
| Backend          | Python, Django                      |
| Frontend         | HTML5, CSS3, JavaScript             |
| Database         | SQLite (default), supports PostgreSQL/MySQL |
| Authentication   | Django's built-in auth system       |
| Version Control  | Git, GitHub                         |

---

## 🖼️ Screenshots

> *(Optional – Add your own screenshots later)*  
> ![Login Page](screenshots/login.png)  
> ![Crime Report Form](screenshots/report-form.png)  
> ![Admin Dashboard](screenshots/admin-dashboard.png)

---

## 💻 Installation

Follow these steps to set up the project locally:

```bash
# 1. Clone the repository
git clone https://github.com/caleb187/crime_repo.git
cd crimeproject

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create a superuser (for admin access)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
