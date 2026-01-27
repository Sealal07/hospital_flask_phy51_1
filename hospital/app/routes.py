from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
from flask_login import current_user, login_required, login_user, logout_user
from .models import User, Doctor, Patient, Specialization, Procedure, Appointment
from .forms import RegisterForm, LoginForm, AppointmentForm
from .extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    form.specialization.choices = [(s.id, s.name) for s in
                                   Specialization.query.all()]
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        if user.role == 'doctor':
            spec_id = form.specialization.data
            doc_name = form.name.data
            doctor = Doctor(
                name=doc_name,
                user_id=user.id,
                specialization_id=spec_id
            )
            db.session.add(doctor)
            db.session.commit()
        elif user.role == 'patient':
            name = form.name.data
            patient = Patient(
                name=name,
                user_id=user.id
            )
            db.session.add(patient)
            db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user) #автоматическая авторизация
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful!', 'danger')
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
        return render_template('doctor_dashboard.html',
                               appointments=appointments, doctor=doctor)
    elif current_user.role == 'patient':
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        appointments = Appointment.query.filter_by(patient_id=patient.id).all()
        return render_template('patient_dashboard.html',
                               appointments=appointments, patient=patient)
    else:
        return render_template('admin.html') #сделать админку

@main.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    if current_user.role != 'patient':
        flash("can't book", 'warning')
        return redirect(url_for('main.dashboard'))

    form = AppointmentForm()
    form.specialization.choices = [(s.id, s.name) for s in Specialization.query.all()]
    if form.specialization.data:
        specialization_id = form.specialization.data
        form.doctor.choices = [(d.id, d.name) for d in Doctor.query.filter_by(
            specialization_id=specialization_id
        ).all()]
        form.procedure.choices = [(p.id, p.name) for p in Procedure.query.filter_by(
            specialization_id=specialization_id
        ).all()]
    else:
        form.doctor.choices = []
        form.procedure.choices = []

    time_slots = [(f'{hour:02d}:{minute:02d}', f'{hour:02d}:{minute:02d}')
                  for hour in range(9, 20) for minute in range(0, 60, 20)]
    form.time_slots = time_slots

    if form.validate_on_submit():
        selected_date = form.date.data.strftime('%Y-%m-%d')
        selected_time = form.time_slot.data
        appointment_time = datetime.strptime(f'{selected_date} {selected_time}')

        booked_store = Appointment.get_time_slots(form.doctor.data, selected_date)
        if selected_time in booked_store:
            flash('already booked', 'danger')
            return render_template('appointment.html', form=form, time_slots=time_slots)

        appointment = Appointment(patient_id=current_user.id,
                                  doctor_id=form.doctor_id.data,
                                  procedure_id=form.procedure.data,
                                  appointment_time=appointment_time)
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment added', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('appointment.html', form=form, time_slots=time_slots)

