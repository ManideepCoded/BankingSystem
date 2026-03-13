🏦 Banking System

A Web-Based Banking Management System built using Django (Python) that allows users to create accounts, manage transactions, transfer money, and apply for loans through a simple web interface.
This project demonstrates full-stack web development using Django, HTML templates, and database models to simulate real banking operations.

🚀 Features
🔐 User Registration & Login
💰 Deposit Money
💸 Withdraw Money
🔁 Transfer Money Between Accounts
📜 Transaction History
🏦 Loan Application System
📊 User Dashboard
🛡️ Secure Form Handling using Django

| Layer     | Technology           |
| --------- | -------------------- |
| Backend   | Django (Python)      |
| Frontend  | HTML, CSS            |
| Database  | SQLite               |
| Framework | Django Web Framework |

📂 Project Structure
bank_system
│
├── bank_project
│   │
│   ├── bank_app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   │
│   │   └── templates
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── dashboard.html
│   │       ├── deposit.html
│   │       ├── withdraw.html
│   │       ├── transfer.html
│   │       ├── transaction_history.html
│   │       └── apply_loan.html
│   │
│   └── bank_project
│       ├── settings.py
│       ├── urls.py
│       ├── asgi.py
│       └── wsgi.py

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/ManideepCoded/BankingSystem.git

2️⃣ Navigate to the Project
cd BankingSystem

3️⃣ Install Dependencies
pip install django

4️⃣ Run Database Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Start the Server
python manage.py runserver

6️⃣ Open in Browser
http://127.0.0.1:8000

📷 Application Pages

The system includes the following pages:
Login Page
Registration Page
User Dashboard
Deposit Page
Withdraw Page
Transfer Money Page
Transaction History Page
Loan Application Page

🔐 Security

Django Form Validation
Secure Authentication System
Protected Views for Logged-in Users

🚀 Future Improvements

Add Online Payment Gateway
Implement OTP / Two-Factor Authentication
Add Admin Analytics Dashboard
Deploy to Cloud (AWS / Heroku)
Add Mobile Banking Support

👨‍💻 Author
Manideep Reddy

GitHub:
https://github.com/ManideepCoded

⭐ Support

If you like this project:
⭐ Star the repository
🐛 Report issues
💡 Suggest improvements
