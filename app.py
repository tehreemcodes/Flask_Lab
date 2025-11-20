from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from flask_bcrypt import Bcrypt # NEW IMPORT

# Ensure you have installed required packages: 
# pip install Flask Flask-SQLAlchemy Flask-WTF email_validator Flask-Bcrypt

app = Flask(__name__)

# ---------- DATABASE & SECRET KEY CONFIGURATION ----------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_lab.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# REQUIRED for WTForms (CSRF protection) and Session encryption
app.config['SECRET_KEY'] = 'a_very_secret_and_long_key_for_csrf_protection_12345'

# ----------------- FIX: SECURE SESSION MANAGEMENT CONFIGURATION -----------------
# 1. Sets the maximum lifetime for permanent sessions to 1 hour (3600 seconds)
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 

# 2. CRITICAL: Ensures the cookie is ONLY sent over HTTPS/SSL (Secure flag)
#    Note: This will prevent the session cookie from being set when running on http://localhost
app.config['SESSION_COOKIE_SECURE'] = True 

# 3. Ensures the cookie is inaccessible via client-side JavaScript (HttpOnly flag)
app.config['SESSION_COOKIE_HTTPONLY'] = True 

# 4. Helps mitigate CSRF risks (SameSite flag)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app) # NEW: Initialize Bcrypt

# ---------- DATABASE MODELS ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    # FIX: Increase column size to safely store Bcrypt hash (~60 chars)
    password = db.Column(db.String(255), nullable=False) 

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

# ---------- WTFORMS FOR SECURE INPUT HANDLING ----------
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=25),
        Regexp('^[A-Za-z0-9_.]*$', 0,
               'Username must contain only letters, numbers, dots or underscores')
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(max=100),
        Regexp("^[A-Za-z\s.\-']+$", 0, 'Name contains invalid characters') 
    ])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone', validators=[
        DataRequired(),
        Length(max=20),
        Regexp('^[0-9()\s\-+]*$', 0, 'Phone number format is invalid')
    ])
    address = TextAreaField('Address', validators=[
        DataRequired(), 
        Length(max=200),
        # Regexp to prevent injection by excluding single quotes (')
        Regexp('^[A-Za-z0-9\s.,\-/]*$', 0, 'Address contains invalid characters')
    ])
    submit = SubmitField('Submit')

# ---------- ROUTES (UPDATED for Session Demo) ----------
@app.route('/')
def home():
    # Show if user is logged in
    status = f"Logged in as: {session.get('username')}" if session.get('logged_in') else "Not logged in."
    # UPDATED security status message
    return f"Hello, Flask is working! Security status: Input Validated, CSRF Protected, Secure Error Handling, Secure Password Storage, {status}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # ----------------- FIX: HASH PASSWORD BEFORE STORAGE -----------------
        # Hash the password using Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # --- SESSION MANAGEMENT: START SESSION ---
        session['logged_in'] = True
        session['username'] = username
        session.permanent = True # This applies the PERMANENT_SESSION_LIFETIME config
        
        # save user to database (storing the HASHED password)
        new_user = User(username=username, password=hashed_password) # Use hashed_password
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('success_message', message=f"User '{username}' registered and secure session attempted!"))
        
    return render_template('login.html', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data

        # save contact details to database
        new_contact = Contact(name=name, email=email, phone=phone, address=address)
        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for('success_message', message=f"Contact for '{name}' saved successfully!"))
        
    return render_template('contact.html', form=form)
    
@app.route('/success/<message>')
def success_message(message):
    return render_template('success.html', message=message)

# ----------------- FIX: SECURE ERROR HANDLERS -----------------
@app.errorhandler(404)
def page_not_found(e):
    # Log the error internally
    app.logger.error(f'404 Not Found: {request.url}')
    # Return a generic, styled 404 page using the error.html Canvas file
    return render_template('error.html', 
                           error_code='404', 
                           error_title='Page Not Found',
                           error_description='The URL you requested does not exist on the server. Please check the address and try again.'), 404

@app.errorhandler(500)
def internal_server_error(e):
    # Log the error internally
    app.logger.error(f'500 Internal Server Error: {e}')
    # Return a generic, styled 500 page (CRITICAL FIX)
    return render_template('error.html', 
                           error_code='500', 
                           error_title='Internal Server Error',
                           error_description='Something went wrong. The server encountered an internal error and was unable to complete your request. Our team has been notified.'), 500


# ---------- RUN APP (NO CHANGE) ----------
if __name__ == '__main__':
    with app.app_context():
        # NOTE: You must delete the existing 'flask_lab.db' file before running, 
        # as the 'password' column size has changed from 100 to 255.
        db.create_all() 
    app.run(debug=False)