# Classification Data Preperation Exercises

import env
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import acquire

def prep_iris(iris):
    iris.drop(columns=['species_id', 'measurement_id'], inplace=True)
    iris.rename(columns={'species_name':'species'}, inplace=True)
    encoder = LabelEncoder()
    encoder.fit(iris.species)
    iris.species = encoder.transform(iris.species)
    return iris

def prep_titanic(titanic):
    titanic.embark_town.fillna('Other', inplace=True)
    titanic.embarked.fillna('Other', inplace=True)
    titanic.drop(columns='deck', inplace=True)
    encoder = LabelEncoder()
    encoder.fit(titanic.embarked)
    titanic.embarked = encoder.transform(titanic.embarked)
    titanic_train, titanic_test = train_test_split(titanic, random_state=seed)
    scaler = MinMaxScaler()
    titanic_train[['fare', 'age']] = scaler.fit_transform(titanic_train[['fare', 'age']])
    return titanic_train, titanic_test, scaler