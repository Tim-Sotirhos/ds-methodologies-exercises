# Feature Engineering Exercises

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
from sklearn.feature_selection import SelectKBest, f_regression
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE

# prep work
telco = wrangle.wrangle_telco()
telco.describe()
telco.set_index('customer_id')

# split data
def split_my_data(telco):
    train, test = train_test_split(df, train_size = 0.8, random_state = 123)
    # assign variable vs target
    X_train = train.drop(columns = 'total_charges')
    y_train = train[['total_charges']]
    X_test = test.drop(columns = 'total_charges')
    y_test = test[['total_charges']]
    return X_train, y_train, X_test, y_test

X_train, y_train, X_test, y_test = split_my_data(telco)

# scale train and test data
def standard_scaler(train, test):
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(train)
    train_scaled_data = scaler.transform(train)
    test_scaled_data = scaler.transform(test)
    train_scaled = pd.DataFrame(train_scaled_data, columns=train.columns).set_index([train.index])
    test_scaled = pd.DataFrame(test_scaled_data, columns=test.columns).set_index([test.index])
    return scaler, train_scaled, test_scaled

scaler, train_scaled, test_scaled = standard_scaler(train, test)

# split scale data
X_train_scaled = train_scaled.drop(columns = "total_charges")
y_train_scaled = train_scaled[["total_charges"]]

X_test_scaled = test_scaled.drop(columns = "total_charges")
y_test_scaled = test_scaled[["total_charges"]]


# 1.) Write a function that takes X_train, y_train and k as input 
# (X_train and y_train should not be scaled!) and returns a list of the top k features.

def select_kbest_freg_unscaled(X_train, y_train, k):
    f_selector = SelectKBest(f_regression, k=k)
    f_selector.fit(X_train, y_train)
    f_support = f_selector.get_support()
    f_feature = X_train.loc[:,f_support].columns.tolist()
    return f_feature, f_selector

select_kbest_freg_unscaled(X_train, y_train, 2)

# 2.) Write a function that takes X_train, y_train (scaled) and k as input 
# and returns a list of the top k features.

def select_kbest_freg_scaled(X_train_scaled, y_train_scaled, k):
    
    f_selector_scaled = SelectKBest(f_regression, k=k)
    
    f_selector.fit(X_train_scaled, y_train_scaled)
    
    f_support = f_selector.get_support()
    
    f_feature_scaled = X_train_scaled.loc[:,f_support].columns.tolist()
    
    return f_feature_scaled, f_selector_scaled

select_kbest_freg_scaled(X_train_scaled,y_train_scaled, 2)


# 3.) Write a function that takes X_train and y_train (scaled) as input 
# and returns selected features based on the ols backwards elimination method.

def ols_backware_elimination():
def ols_backware_elimination(X_train, y_train):
    
    import statsmodels.api as sm
    # create the OLS object:
    ols_model = sm.OLS(y_train, X_train)

    # fit the model:
    fit = ols_model.fit()

    # summarize:
    fit.summary()
    
    cols = list(X_train_scaled.columns)
    pmax = 1

    while (len(cols)>0):
        X_1 = X_train[cols]
        model = sm.OLS(y_train,X_1).fit()
        p = model.pvalues
        pmax = max(p)
        feature_with_p_max = p.idxmax()
        if(pmax>0.05):
            cols.remove(feature_with_p_max)
        else:
            break

    selected_features_BE = cols    
    return selected_features_BE

ols_backware_elimination(X_train_sc, y_train_sc)

# 4.) Write a function that takes X_train and y_train as input and returns the coefficients for each feature, along with a plot of the features and their weights.

def lasso_cv_coef():

model = LinearRegression()

#Initializing RFE model, with parameter to select top 2 features. 
rfe = RFE(model, 2)

#Transforming data using RFE
X_rfe = rfe.fit_transform(X_train,y_train) 

#Fitting the data to model
model.fit(X_rfe,y_train)

print(rfe.support_)
print(rfe.ranking_)

# 5.) Write 3 functions, 
# the first computes the number of optimum features (n) using rfe, 
# the second takes n as input and returns the top n features, 
# and the third takes the list of the top n features as input and returns a new X_train and X_test dataframe with those top features , recursive_feature_elimination() that computes the optimum number of features (n) and returns the top n features.


number_of_features_list=np.arange(1,3)
high_score=0

#Variable to store the optimum features
number_of_features=0           
score_list =[]

for n in range(len(number_of_features_list)):
    model = LinearRegression()
    rfe = RFE(model,number_of_features_list[n])
    X_train_rfe = rfe.fit_transform(X_train,y_train)
    X_test_rfe = rfe.transform(X_test)
    model.fit(X_train_rfe,y_train)
    score = model.score(X_test_rfe,y_test)
    score_list.append(score)
    if(score>high_score):
        high_score = score
        number_of_features = number_of_features_list[n]

print("Optimum number of features: %d" %number_of_features)
print("Score with %d features: %f" % (number_of_features, high_score))