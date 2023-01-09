from flask import Blueprint
from flask import current_app, render_template, url_for, flash, redirect, request
from dashboardapp.dbmodels import User, APIUsage, Datasets, Encryption
from dashboardapp import db, CHART_OPTIONS, ADMIN_EMAIL
from flask_login import current_user, login_required
from dashboardapp.main.utils import *


main = Blueprint('main', __name__)

# Route for the dashboard page
@main.route("/dashboard", methods = ['GET','POST'])
@login_required
def dashboard():
    # database count
    if current_user.email ==ADMIN_EMAIL:
        db_count = Datasets.query.count()
        user_count = User.query.count()
        api_count = APIUsage.query.count()
        # Encryption type is used to specify 'Statistics', 'Visualization', 'Encrypt-decrypt', 'Training', 'Inference'
        statistics_count = APIUsage.query.filter_by(call_type ='statistics').count()
        visualization_count = APIUsage.query.filter_by(call_type ='Visualization').count()
        encryption_count = APIUsage.query.filter_by(call_type ='Encrypt-decrypt').count()
        training_count = APIUsage.query.filter_by(call_type ='Training').count()
        inference_count = APIUsage.query.filter_by(call_type ='Inference').count()
        alerts = 0 # dummy value
    else:
        db_count = Datasets.query.filter_by(user_id=current_user.id).count()
        user_count = 1
        api_count = APIUsage.query.filter_by(user_id=current_user.id).count()
        alerts = 0

        statistics_count = APIUsage.query.filter_by(call_type ='statistics',user_id=current_user.id).count()
        visualization_count = APIUsage.query.filter_by(call_type ='Visualization',user_id=current_user.id).count()
        encryption_count = APIUsage.query.filter_by(call_type ='Encrypt-decrypt',user_id=current_user.id).count()
        training_count = APIUsage.query.filter_by(call_type ='Training',user_id=current_user.id).count()
        inference_count = APIUsage.query.filter_by(call_type ='Inference',user_id=current_user.id).count()
    
    api_calls = {'Statistics':statistics_count, 
                'Visualization':visualization_count, 
                'Encrypt-decrypt':encryption_count, 
                'Training':training_count, 
                'Inference':inference_count}
    print(list(api_calls.keys()))           
    return render_template("home.html", title='Encryption Dashboard',
                             db_count=db_count, user_count=user_count, 
                             api_count=api_count, alerts = alerts, 
                             api_calls_values=list(api_calls.values()),
                             api_calls_keys= list(api_calls.keys()))




# Dataset route
@main.route("/dataset", methods=['GET', 'POST'])
@login_required
def dataset():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_ext = os.path.splitext(uploaded_file.filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                warning='File upload unsuccessful! Supported file formats: ' + " | ".join(current_app.config['UPLOAD_EXTENSIONS'])
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


# Route for each dataset
@main.route("/dataset/<int:dataset_id>",methods=['GET', 'POST'])
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
            file_path = os.path.join(current_app.root_path, 'static/datasets', dataset.filename)
            key, nonce = encrypt_data(file_path)
            # print(f"Key: {key}")
            # print(f"Nonce: {nonce}")

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
            return redirect(url_for('main.dataview', dataset_id=dataset.id))
        
    return render_template('dataview.html', title=dataset.filename, df_html=df_html, dataset_encrypted = dataset.is_encrypted)



# Dataset route
@main.route("/keyaccess", methods=['GET', 'POST'])
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
        keys = [Encryption.query.filter_by(dataset_id=dataset.id).first() for dataset in datasets]
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

    num_keys = len(key_access_status)
    return render_template('keys.html', title='Keys', warning=warning, keys=key_access_status, num_keys=num_keys)




# Dataset route
@main.route("/visualization", methods=['GET', 'POST'])
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
        #print(sub_dataset)
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

        #print(selected_dataset)

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
    #print(labels)
    #print(values)
    


    return render_template('visualization.html', title='Visualization', 
                            warning=warning, datasets = datasets, 
                            chart_options= CHART_OPTIONS, selected_chart = chartype_chosen,
                            columns=columns, selected_column= selected_column,
                            selected_dataset=selected_dataset,
                            labels=labels, values=values)

# Route for plotting the graph
@main.route("/plotting/<filename>", methods=['GET', 'POST'])
@login_required
def plotting(filename):
    print('Plotting')
    chartype_chosen = request.form['chart-type']
    print(filename)
    print(chartype_chosen)
    return redirect(url_for('main.visualization'))
    #return render_template('plotting.html', title='Plotting')


# Dataset route
@main.route("/terminal", methods=['GET', 'POST'])
@login_required
def terminal():
    if request.method == 'POST':

        print('POST TODOD')
        warning=''
    else:
        warning=''
    return render_template('terminal.html', title='Terminal', warning=warning)


# Dataset route
@main.route("/help", methods=['GET', 'POST'])
@login_required
def help():
    if request.method == 'POST':

        print('POST TODOD')
        warning=''
    else:
        warning=''
    return render_template('help.html', title='Help', warning=warning)


