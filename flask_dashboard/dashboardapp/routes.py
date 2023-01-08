from flask import render_template, url_for, flash, redirect, request
from dashboardapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from dashboardapp.dbmodels import User, APIUsage, Datasets, Encryption
from dashboardapp import app, db, bcrypt, CHART_OPTIONS, ADMIN_EMAIL
from flask_login import login_user, current_user, logout_user, login_required
from dashboardapp.encryption import encrypt_data, decrypt_data
from dashboardapp.plots import get_histogram
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
    # database count
    if current_user.email ==ADMIN_EMAIL:
        db_count = Datasets.query.count()
        user_count = User.query.count()
        api_count = APIUsage.query.count()
        alerts = 2 # dummy value
    else:
        db_count = Datasets.query.filter_by(user_id=current_user.id).count()
        user_count = 1
        api_count = APIUsage.query.filter_by(user_id=current_user.id).count()
        alerts = 2
    return render_template("home.html", title='Encryption Dashboard', db_count=db_count, user_count=user_count, api_count=api_count, alerts = alerts)

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
        print('POST TODO')
    else:
        warning=''
    
    # Get the datasets from the database
    if current_user.email ==ADMIN_EMAIL:
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


# Get column names

def get_column_names(dataset):
    file_path = os.path.join(app.root_path, 'static/datasets', dataset.filename)
    # Load the csv file to pandas dataframe
    df=pd.read_csv(file_path)
    column_names = df.columns.values.tolist()
    return column_names

def get_data_for_plotting(selected_dataset, chartype_chosen):
    file_path = os.path.join(app.root_path, 'static/datasets', selected_dataset['filename'])
    # Load the csv file to pandas dataframe


    dataset = Datasets.query.filter_by(filename=selected_dataset['filename']).first()

    key = Encryption.query.filter_by(dataset_id=dataset.id).first()
    # print(chartype_chosen)
    # print(dataset)
    # print(key.encryption_key)
    # print(key.encryption_nonce)
    decrypted_data = decrypt_data(file_path, key.encryption_key, key.encryption_nonce)

    # Just focus on the age column for now
    col=[]
    for row in decrypted_data[1:]:
            try:
                col.append(float(row[int(selected_dataset['column'])+1])) #1 because the first column is the index
            except ValueError:
                col.append(row[int(selected_dataset['column'])+1]) #1 because the first column is the index

    # Return the age column
    print(col)
    # Get the histogram
    if chartype_chosen == 'HISTOGRAM':
        if type(col[0]) != float:
            return [], []
        hist, bin_edges = get_histogram(col)
        labels=bin_edges.tolist()[:-1] #Remember to undo this
        labels=[round(i,2) for i in labels]
        values=hist.tolist()
    elif chartype_chosen =='PIE CHART':
        df = pd.DataFrame({'col':col})
        if type(col[0]) == float:
            # print(df['col'].unique())
            labels=[]
            values=col
        elif type(col[0]) == str:
            labels = df['col'].value_counts().keys().tolist()
            values = df['col'].value_counts().tolist()
            values = [int(v) for v in values]
            return [], values
        else:
            labels = []
            values = []
    else:
        labels=[]
        values=[]
    return labels, values



# Dataset route
@app.route("/visualization", methods=['GET', 'POST'])
@login_required
def visualization():
    
    # Get the accessable datasets from the database
    if current_user.email ==ADMIN_EMAIL:
        datasets = Datasets.query.all()
    else:
        datasets = Datasets.query.filter_by(user_id=current_user.id)


    if request.method == 'POST':
        filename_chosen = request.form['dataset-filename']
        print(filename_chosen)
        sub_dataset = Datasets.query.filter_by(filename=filename_chosen, user_id=current_user.id).first()
        print(sub_dataset)
        warning=''
        columns = get_column_names(sub_dataset)[1:]
        
        chartype_chosen = request.form['chart-type']
        selected_column = request.form['column-name']

        if selected_column in columns:
            selected_dataset = {"filename":filename_chosen,
                                "column":columns.index(selected_column)}
        else:
            selected_dataset = {"filename":filename_chosen,
                                "column":0}

        print(selected_dataset)

        #print(chartype_chosen)
            # Update the database recording API calls
        apiuse = APIUsage(num_of_calls= 1, call_type='Visualization', api_contents = chartype_chosen, user_id=current_user.id)
        db.session.add(apiuse)
        db.session.commit()


    # This is for the GET method
    else:
        #print(columns)
        warning=''
        temp = 0 # Age column for temporary
        columns = get_column_names(datasets[0])[1:]
        selected_column = columns[temp]
        selected_dataset = {"filename":datasets[temp].filename,
                            "column":temp}
        chartype_chosen = 'HISTOGRAM'

    
    
    
    # data for plotting
    labels, values= get_data_for_plotting(selected_dataset, chartype_chosen)
    # data = [(0,1), (1,10), (2,5), (3,19)]
    # labels = [row[0] for row in data]
    # values = [row[1] for row in data]
    print(labels)
    print(values)
    


    return render_template('visualization.html', title='Visualization', 
                            warning=warning, datasets = datasets, 
                            chart_options= CHART_OPTIONS, selected_chart = chartype_chosen,
                            columns=columns, selected_column= selected_column,
                            selected_dataset=selected_dataset,
                            labels=labels, values=values)

# Route for plotting the graph
@app.route("/plotting/<filename>", methods=['GET', 'POST'])
@login_required
def plotting(filename):
    print('Plotting')
    chartype_chosen = request.form['chart-type']
    print(filename)
    print(chartype_chosen)
    return redirect(url_for('visualization'))
    #return render_template('plotting.html', title='Plotting')


# Dataset route
@app.route("/terminal", methods=['GET', 'POST'])
@login_required
def terminal():
    if request.method == 'POST':

        print('POST TODOD')
        warning=''
    else:
        warning=''
    return render_template('terminal.html', title='Terminal', warning=warning)


