# Scaling Numeric Data exercise

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import wrangle
import env
import math
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer,RobustScaler,MinMaxScaler

df = wrangle.wrangle_telco()
df.info()
df.describe()
df.head()
df = df.set_index('customer_id')
df

# 1.) split_my_data(X, y, train_pct)

x = df.drop(columns = 'total_charges')
y = df.total_charges

x_train, x_test, y_train, y_test = train_test_split(x,y, train_size = .80, random_state = 123)

# Or just x_train and x_test

train, test = train_test_split(df, train_size= .80, random_state= 123)

print(train.shape)
print(test.shape)

# 2.) standard_scaler()

# Create the scaler object

scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(train)

# Print the parameters

print("Mean Train:")
print(scaler.mean_)

print("Standard Deviation Train:")
print([math.sqrt(i) for i in scaler.var_])

# Transform the train and test data sets into a np.array

train_scaled_data = scaler.transform(train)

test_scaled_data = scaler.transform(test)

# Create pd.DataFrame from the transformed train and test data sets

train_scaled = pd.DataFrame(train_scaled_data, columns=train.columns).set_index([train.index])

test_scaled = pd.DataFrame(test_scaled_data, columns=test.columns.values).set_index([test.index.values])

# 3.) scale_inverse()

train_unscaled = pd.DataFrame(scaler.inverse_transform(train_scaled), columns=train_scaled.columns).set_index([train.index])
test_unscaled = pd.DataFrame(scaler.inverse_transform(test_scaled), columns=test_scaled.columns).set_index([test.index])

# 4.) uniform_scaler()

scaler = QuantileTransformer(n_quantiles=100, output_distribution='uniform', random_state=123, copy=True).fit(train)

train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])

# 5.) gaussian_scaler()

scaler = PowerTransformer(method='yeo-johnson', standardize=False, copy=True).fit(train)

train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])

test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])

# 6.) min_max_scaler()

scaler = MinMaxScaler(copy=True, feature_range=(0,1)).fit(train)

train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])

test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])

# 7.) iqr_robust_scaler()

scaler = RobustScaler(quantile_range=(25.0,75.0), copy=True, with_centering=True, with_scaling=True).fit(train)

train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])

test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])