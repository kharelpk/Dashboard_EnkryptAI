from flask import render_template, url_for, flash, redirect, request
from dashboardapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from dashboardapp.dbmodels import User, APIUsage, Datasets, Encryption
from dashboardapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from dashboardapp.encryption import encrypt_data
import secrets
import os
from PIL import Image
import pandas as pd


# Defeault webpage starts at the login page
@app.route("/")
@app.route("/login", methods = ['GET', 'POST'])
def login():
    # If the user is authenticated, redirect to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.','danger')
    return render_template("login.html",title='Login',form=form)



# Route for the register page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    # If the user is authenticated, redirect to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

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
@login_required
def dashboard():
    return render_template("home.html", title='Encryption Dashboard')

# Route for the dashboard page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# Account route
@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='images/profile_pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/profile_pictures', picture_filename)
    
    output_size = (75, 75)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename

# Account route
@app.route("/update_account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/profile_pictures/' + current_user.image_file)
    return render_template('update_account.html', title='Update Account', image_file=image_file, form=form)


# Save the dataset to the database
def save_dataset(uploaded_file):
    # Save the dataset to the database
    file_path = os.path.join(app.root_path, 'static/datasets', uploaded_file.filename)
    uploaded_file.save(file_path)
    return uploaded_file.filename

# Dataset route
@app.route("/dataset", methods=['GET', 'POST'])
@login_required
def dataset():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_ext = os.path.splitext(uploaded_file.filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                warning='File upload unsuccessful! Supported file formats: ' + " | ".join(app.config['UPLOAD_EXTENSIONS'])
            else:
                # Save the dataset locally
                fn= save_dataset(uploaded_file)
                # Update the database
                new_dataset = Datasets(filename=fn, user_id=current_user.id)
                db.session.add(new_dataset)
                db.session.commit()
                warning='File uploaded successfully.'
    else:
        warning=''
    
    # Get the datasets from the database
    if current_user.email =='admin@admin.com':
        datasets = Datasets.query.all()
    else:
        datasets = Datasets.query.filter_by(user_id=current_user.id)


    return render_template('dataset.html', title='Dataset', warning=warning, datasets=datasets)

# Generate pandas dataframe and display it
def generate_dataframe(dataset):
    file_path = os.path.join(app.root_path, 'static/datasets', dataset.filename)
    # Load the csv file to pandas dataframe
    df=pd.read_csv(file_path)

    #print(df.head(10))
    # print(df.to_html(classes='mystyle'))
    
    return df, df.head(10).to_html(border=0, classes= "mytablestyle")


# Route for each dataset
@app.route("/dataset/<int:dataset_id>",methods=['GET', 'POST'])
@login_required
def dataview(dataset_id):
    dataset = Datasets.query.get_or_404(dataset_id)
    if dataset:
        # Generate a pandas dataframe
        df , df_html = generate_dataframe(dataset)
        #print(df_html)
    if request.method == 'POST':
        # Check if the data is already encrypted
        # If not, encrypt the data
        # Update the database
        if not dataset.is_encrypted:
            # Encrypt data here
            print(f"Encrypting the {dataset.filename}")
            file_path = os.path.join(app.root_path, 'static/datasets', dataset.filename)
            key, nonce = encrypt_data(file_path)
            print(f"Key: {key}")
            print(f"Nonce: {nonce}")

            # Update dataset to make sure it says it's encrypted
            dataset.is_encrypted = True
            
            # Update the key database
            new_key = Encryption(dataset_id=dataset_id, encryption_key = key, encryption_nonce = nonce)
            
            # Update the database recording API calls
            apiuse = APIUsage(num_of_calls= 1, call_type='Encrypt-decrypt', api_contents = '', user_id=current_user.id)
            
            db.session.add(new_key)
            db.session.add(apiuse)
            db.session.commit()

            # Return the user back to the dataset page to show encrypted data
            return redirect(url_for('dataview', dataset_id=dataset.id))
        
    return render_template('dataview.html', title=dataset.filename, df_html=df_html, dataset_encrypted = dataset.is_encrypted)



    # Dataset route
@app.route("/keyaccess", methods=['GET', 'POST'])
@login_required
def keyaccess():
    if request.method == 'POST':
        
        print('POST TODOD')
    else:
        warning=''
    
    # Get the datasets from the database
    if current_user.email =='admin@admin.com':
        datasets = Datasets.query.all()
        keys = Encryption.query.all()

        key_access_status = []
        for key in keys:
            dataset_id = key.dataset_id
            dataset = Datasets.query.get_or_404(dataset_id)
            dictionary ={
                "key_id": key.id,
                "filename": dataset.filename,
                "num_users": User.query.count()
            }
            key_access_status.append(dictionary)
    else:
        datasets = Datasets.query.filter_by(user_id=current_user.id)


    return render_template('keys.html', title='Keys', warning=warning, keys=key_access_status)
