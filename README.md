# Thikse Field Visit Tracker System

A complete web application developed for Thikse Company to manage employee attendance, log client visits, and generate daily field activity reports. 

## Features
- **Employee Module**: Log daily attendance (Check-in/Check-out), record client visits, update status.
- **Admin Module**: Monitor employee visits, search and filter records, track overall field activities.
- **Responsive UI**: Built with Bootstrap 5.

## Technologies Used
- Python 3.11+
- Flask & Flask-SQLAlchemy (Backend & ORM)
- SQLite (Database - can be easily migrated to MySQL/PostgreSQL)
- HTML5, CSS3, Bootstrap 5 (Frontend)
- Flask-Login & Flask-Bcrypt (Authentication & Security)

## Installation & Setup

1. **Clone the repository / Extract files**
2. **Create a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Initialize Database:**
   ```bash
   python init_db.py
   ```
   *This creates the `instance/tracker.db` file (SQLite) and sets up mock accounts:*
   - Admin: `admin@thikse.com` / `admin123`
   - Employee: `employee@thikse.com` / `emp123`
5. **Run the Application:**
   ```bash
   python app.py
   ```
6. **Access:** Open `http://127.0.0.1:5000` in your browser.

## Database Schema (SQL)
*(Refer to `database.sql` for the raw SQL dump, generated via sqlite3 dump).*
