from app import app, db
from models import Employee
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if admin exists
        admin = Employee.query.filter_by(email='admin@thikse.com').first()
        if not admin:
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = Employee(name='System Admin', email='admin@thikse.com', password=hashed_password, role='admin')
            db.session.add(admin)
            
        # Check if employee exists
        employee = Employee.query.filter_by(email='employee@thikse.com').first()
        if not employee:
            hashed_password = bcrypt.generate_password_hash('emp123').decode('utf-8')
            employee = Employee(name='Test Employee', email='employee@thikse.com', password=hashed_password, role='employee')
            db.session.add(employee)
            
        db.session.commit()
        print("Database initialized with admin and test employee.")

if __name__ == '__main__':
    init_db()
