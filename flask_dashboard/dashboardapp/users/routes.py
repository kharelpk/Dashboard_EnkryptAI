from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from dashboardapp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from dashboardapp.dbmodels import User
from flask_login import login_user, current_user, logout_user, login_required
from dashboardapp import db, bcrypt
from dashboardapp.users.utils import save_picture

users = Blueprint('users', __name__)


# Defeault webpage starts at the login page
@users.route("/")
@users.route("/login", methods = ['GET', 'POST'])
def login():
    # If the user is authenticated, redirect to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the email exists in the database
        user = User.query.filter_by(email=form.email.data).first()
        # If the email exists, check the password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # If the password is correct, redirect to the dashboard
            #flash('Login Successful.', 'success')
            login_user(user, remember=form.remember.data)
            # Redirect to the next page if it exists
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.','danger')
    return render_template("login.html",title='Login',form=form)



# Route for the register page
@users.route("/register", methods = ['GET', 'POST'])
def register():
    # If the user is authenticated, redirect to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

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
        return redirect(url_for('users.login'))

    return render_template("register.html", title='Register', form= form)

# Route for the dashboard page
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


# Account route
@users.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='images/profile_pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)



# Account route
@users.route("/update_account", methods=['GET', 'POST'])
@login_required
def update_account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        # If picture was uploaded save the picture to profile_pictures directory
        # Then update the image_file column in the database
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
            current_user.image_file = picture_filename
        
        # Update the user's information in the database
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/profile_pictures/' + current_user.image_file)
    return render_template('update_account.html', title='Update Account', image_file=image_file, form=form)

