from dashboardapp.encryption import encrypt_data, decrypt_data
from dashboardapp.dbmodels import Datasets, Encryption
from flask import current_app
import pandas as pd
import numpy as np
import os


def get_histogram(data):
    # Get the histogram of the data
    hist, bin_edges = np.histogram(data)
    return hist, bin_edges

# Save the dataset to the database
def save_dataset(uploaded_file):
    # Save the dataset to the database
    file_path = os.path.join(current_app.root_path, 'static/datasets', uploaded_file.filename)
    uploaded_file.save(file_path)
    return uploaded_file.filename


# Generate pandas dataframe and display it
def generate_dataframe(dataset):
    file_path = os.path.join(current_app.root_path, 'static/datasets', dataset.filename)
    # Load the csv file to pandas dataframe
    df=pd.read_csv(file_path)

    #print(df.head(10))
    # print(df.to_html(classes='mystyle'))
    
    return df, df.head(10).to_html(border=0, classes= "mytablestyle")


# Get column names

def get_column_names(dataset):
    file_path = os.path.join(current_app.root_path, 'static/datasets', dataset.filename)
    # Load the csv file to pandas dataframe
    df=pd.read_csv(file_path)
    column_names = df.columns.values.tolist()
    return column_names

def get_data_for_plotting(selected_dataset, chartype_chosen):
    file_path = os.path.join(current_app.root_path, 'static/datasets', selected_dataset['filename'])
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
    #print(col)
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
