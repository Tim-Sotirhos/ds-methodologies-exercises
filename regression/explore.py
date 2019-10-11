# Exploration exercises

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.filterwarnings("ignore")

import env
import wrangle
import split_scale

# acquire data and remove null values
df = wrangle.wrangle_telco()
# split into train and test
train, test = split_scale.split_my_data_whole(df, .80)
df.info()
train.info()

# Write a function, plot_variable_pairs(dataframe) that plots all of the pairwise relationships along with the regression line for each pair.

def plot_variable_pairs(df):
    g = sns.PairGrid(df)
    g.map(sns.regplot)
    plt.show()

plot_variable_pairs(df)

# Write a function, months_to_years(tenure_months, df) that returns your dataframe with a new feature tenure_years, in complete years as a customer.

def months_to_year(df):
    df['tenure_years'] = round(df.tenure//12).astype('category')
    return df

months_to_year(df).head()

# Write a function, plot_categorical_and_continous_vars(categorical_var, continuous_var, df), that outputs 3 different plots for plotting a categorical variable with a continuous variable, e.g. tenure_years with total_charges. For ideas on effective ways to visualize categorical with continuous:

def plot_categorical_and_continous_vars(categorical_var, continuous_var, df):
    
plot
