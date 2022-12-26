from flask import render_template, url_for, flash, redirect
from dashboardapp.forms import RegistrationForm, LoginForm
from dashboardapp.dbmodels import User, APIUsage
from dashboardapp import app, db, bcrypt

# Defeault webpage starts at the login page
@app.route("/")
@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@enkryptai.com' and form.password.data=="password":
            #flash(f'You have been logged in!','success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.','danger')
    return render_template("login.html",title='Login',form=form)



# Route for the register page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password from the form
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create a user and add them to the database
        user = User(firstname = form.firstname.data, lastname = form.lastname.data, email = form.email.data, password = hashed_password) 
        db.session.add(user)
        db.session.commit()
        # Also calls the class 
        flash(f'Your account has been created! Please log in to continue.', "success")
        return redirect(url_for('login'))

    return render_template("register.html", title='Register', form= form)



# Route for the dashboard page
@app.route("/dashboard", methods = ['GET','POST'])
def dashboard():
    return render_template("index.html", title='Encryption Dashboard')


