from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.datetime import DateField

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[('patient', 'Patient'), ('doctor', 'Doctor')], validators=[DataRequired()])
    specialization = SelectField('Specialization', choices=[], coerce=int)
    submit = SubmitField('Registration')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class AppointmentForm(FlaskForm):
    specialization = SelectField('Specialization', choices=[], coerce=int)
    doctor_id = SelectField('Doctor', coerce=int, choices=[])
    procedure = SelectField('Procedure', coerce=int, choices=[])
    date = DateField('Date', format='%Y-%m-%d')
    time_slot = SelectField('Time Slot', choices=[])
    submit = SubmitField('Appointment')