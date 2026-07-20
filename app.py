import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, Employee, Attendance, ClientVisit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thikse-secret-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Employee, int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Employee.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    today = date.today()
    my_visits = ClientVisit.query.filter_by(employee_id=current_user.id).all()
    total_visits = len(my_visits)
    completed_visits = len([v for v in my_visits if v.status == 'Completed'])
    pending_visits = len([v for v in my_visits if v.status == 'Pending'])
    
    today_attendance = Attendance.query.filter_by(employee_id=current_user.id, date=today).first()
    attendance_status = "Not Checked In"
    if today_attendance:
        if today_attendance.check_out:
            attendance_status = "Checked Out"
        elif today_attendance.check_in:
            attendance_status = "Checked In"
            
    return render_template('dashboard.html', 
                           total=total_visits, 
                           completed=completed_visits, 
                           pending=pending_visits,
                           attendance_status=attendance_status)

@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    today = date.today()
    record = Attendance.query.filter_by(employee_id=current_user.id, date=today).first()
    
    if request.method == 'POST':
        action = request.form.get('action')
        now = datetime.now()
        
        if action == 'check_in':
            if not record:
                new_record = Attendance(employee_id=current_user.id, date=today, check_in=now)
                db.session.add(new_record)
                db.session.commit()
                flash('Checked in successfully!', 'success')
            else:
                flash('Already checked in today.', 'warning')
        elif action == 'check_out':
            if record and not record.check_out:
                record.check_out = now
                db.session.commit()
                flash('Checked out successfully!', 'success')
            else:
                flash('Cannot check out. Make sure you are checked in and not already checked out.', 'warning')
        
        return redirect(url_for('attendance'))
        
    history = Attendance.query.filter_by(employee_id=current_user.id).order_by(Attendance.date.desc()).all()
    return render_template('attendance.html', record=record, history=history)

@app.route('/visits', methods=['GET', 'POST'])
@login_required
def visits():
    if request.method == 'POST':
        client_name = request.form.get('client_name')
        company_name = request.form.get('company_name')
        contact_number = request.form.get('contact_number')
        location = request.form.get('location')
        visit_date_str = request.form.get('visit_date')
        purpose = request.form.get('purpose')
        meeting_notes = request.form.get('meeting_notes', '')
        status = request.form.get('status', 'Pending')
        
        try:
            v_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date() if visit_date_str else date.today()
        except ValueError:
            v_date = date.today()
            
        visit = ClientVisit(
            employee_id=current_user.id,
            client_name=client_name,
            company_name=company_name,
            contact_number=contact_number,
            location=location,
            visit_date=v_date,
            purpose=purpose,
            meeting_notes=meeting_notes,
            status=status
        )
        db.session.add(visit)
        db.session.commit()
        flash('Visit recorded successfully!', 'success')
        return redirect(url_for('visits'))
        
    my_visits = ClientVisit.query.filter_by(employee_id=current_user.id).order_by(ClientVisit.visit_date.desc()).all()
    return render_template('visits.html', visits=my_visits)

@app.route('/visits/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_visit(id):
    visit = db.session.get(ClientVisit, id)
    if not visit or (visit.employee_id != current_user.id and current_user.role != 'admin'):
        abort(403)
        
    if request.method == 'POST':
        visit.client_name = request.form.get('client_name')
        visit.company_name = request.form.get('company_name')
        visit.contact_number = request.form.get('contact_number')
        visit.location = request.form.get('location')
        visit.purpose = request.form.get('purpose')
        visit.meeting_notes = request.form.get('meeting_notes', '')
        visit.status = request.form.get('status', 'Pending')
        
        visit_date_str = request.form.get('visit_date')
        if visit_date_str:
            visit.visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
            
        db.session.commit()
        flash('Visit updated successfully!', 'success')
        if current_user.role == 'admin':
            return redirect(url_for('admin_visits'))
        return redirect(url_for('visits'))
        
    return render_template('edit_visit.html', visit=visit)

@app.route('/visits/delete/<int:id>', methods=['POST'])
@login_required
def delete_visit(id):
    visit = db.session.get(ClientVisit, id)
    if not visit or (visit.employee_id != current_user.id and current_user.role != 'admin'):
        abort(403)
        
    db.session.delete(visit)
    db.session.commit()
    flash('Visit deleted successfully!', 'success')
    if current_user.role == 'admin':
        return redirect(url_for('admin_visits'))
    return redirect(url_for('visits'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)
    emp_count = Employee.query.filter_by(role='employee').count()
    visit_count = ClientVisit.query.count()
    today_attendance_count = Attendance.query.filter_by(date=date.today()).count()
    return render_template('admin_dashboard.html', emp_count=emp_count, visit_count=visit_count, today_attendance_count=today_attendance_count)

@app.route('/admin/employees', methods=['GET'])
@login_required
def admin_employees():
    if current_user.role != 'admin':
        abort(403)
    search = request.args.get('search', '')
    if search:
        employees = Employee.query.filter(Employee.name.ilike(f'%{search}%'), Employee.role=='employee').all()
    else:
        employees = Employee.query.filter_by(role='employee').all()
    return render_template('admin_employees.html', employees=employees, search=search)

@app.route('/admin/attendance', methods=['GET'])
@login_required
def admin_attendance():
    if current_user.role != 'admin':
        abort(403)
    filter_date = request.args.get('date', '')
    query = Attendance.query.join(Employee)
    if filter_date:
        try:
            d = datetime.strptime(filter_date, '%Y-%m-%d').date()
            query = query.filter(Attendance.date == d)
        except ValueError:
            pass
    records = query.order_by(Attendance.date.desc()).all()
    return render_template('admin_attendance.html', records=records, filter_date=filter_date)

@app.route('/admin/visits', methods=['GET'])
@login_required
def admin_visits():
    if current_user.role != 'admin':
        abort(403)
    filter_date = request.args.get('date', '')
    search = request.args.get('search', '')
    query = ClientVisit.query.join(Employee)
    if search:
        query = query.filter(Employee.name.ilike(f'%{search}%'))
    if filter_date:
        try:
            d = datetime.strptime(filter_date, '%Y-%m-%d').date()
            query = query.filter(ClientVisit.visit_date == d)
        except ValueError:
            pass
    visits = query.order_by(ClientVisit.visit_date.desc()).all()
    return render_template('admin_visits.html', visits=visits, search=search, filter_date=filter_date)

if __name__ == '__main__':
    app.run(debug=True)
