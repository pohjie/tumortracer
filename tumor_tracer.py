import numpy as np
import pandas as pd
from sklearn import svm

import pdb
import random

def read_data():
    data = pd.read_table('CosmicMutantExport.tsv', sep='\t', header=0, low_memory=False)
    return data

def preprocess(data):
    # We shall begin by removing those labeled 'n' for "Genome.wide.screen".
    data = data.loc[(data['Genome-wide screen'] == 'y') & (data['Sample Type'] != 'cell-line') & (data['Mutation Description'] != 'Substitution - coding silent')]
    
    # further preprocessing, whereby we go by several criteria, then only have a one one relationship between ID_sample and ID_tumour
    data = data.loc[(data['Sample Type'] != 'xenograft') & (data['Mutation somatic status'] == 'Confirmed somatic variant') & (data['Tumour origin'] == 'primary')]

    # get one to one relationship between ID_tumour and ID_sample
    ID_tumour_list = data['ID_tumour'].unique()
    for ID_tumour in ID_tumour_list:
        ID_sample_list = (data.loc[data['ID_tumour'] == ID_tumour])['ID_sample'].unique()
        num_unique_ID_sample = len(ID_sample_list)
        if num_unique_ID_sample > 1:
            chosen_ID_sample = ID_sample_list[random.randint(0, num_unique_ID_sample-1)]
            data.drop(data[(data['ID_tumour'] == ID_tumour) & (data['ID_sample'] != chosen_ID_sample)].index, inplace=True)

    # drop unnecessary columns
    X= data[['ID_tumour', 'Mutation ID', 'Tumour origin']]
    y = data['Primary site']

    # one hot encoding
    X_ohe = pd.get_dummies(X, columns=['Mutation ID', 'Tumour origin'], sparse=True)
    y_ohe = pd.get_dummies(y, sparse=True)

    lin_clf = svm.LinearSVC()
    lin_clf.fit(X_ohe, y_ohe)
    
    pdb.set_trace()

if __name__ == '__main__':
    data = read_data()
    preprocessed_data = preprocess(data)