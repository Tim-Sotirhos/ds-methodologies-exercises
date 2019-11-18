import acquire
import pandas as pd

from datetime import timedelta, datetime
import numpy as np

# Code from the summarize.py module

def nulls_by_col(df):
    num_missing = df.isnull().sum()
    rows = df.shape[0]
    pct_missing = num_missing/rows
    cols_missing = pd.DataFrame({'num_rows_missing': num_missing, 'pct_rows_missing': pct_missing})
    return cols_missing

def nulls_by_row(df):
    num_cols_missing = df.isnull().sum(axis=1)
    pct_cols_missing = df.isnull().sum(axis=1)/df.shape[1]*100
    rows_missing = pd.DataFrame({'num_cols_missing': num_cols_missing, 'pct_cols_missing': pct_cols_missing}).reset_index().groupby(['num_cols_missing','pct_cols_missing']).count().rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return rows_missing

def df_value_counts(df):
    counts = pd.Series([])
    for i, col in enumerate(df.columns.values):
        if df[col].dtype == 'object':
            col_count = df[col].value_counts()
        else:
            col_count = df[col].value_counts(bins=10, sort=False)
        counts = counts.append(col_count)
    return counts

def df_summary(df):
    print('--- Shape: {}'.format(df.shape))
    print('--- Info')
    df.info()
    print('--- Descriptions')
    print(df.describe(include='all'))
    print('--- Nulls By Column')
    print(nulls_by_col(df))
    print('--- Nulls By Row')
    print(nulls_by_row(df))
    print('--- Value Counts')
    print(df_value_counts(df))


def prep_store_data(df):
    #parse the date column and set it as the index
    fmt = '%a, %d %b %Y %H:%M:%S %Z'

    df.sale_date = pd.to_datetime(df.sale_date, format= fmt)

    df = df.sort_values(by='sale_date').set_index('sale_date')
    
    # add some time components as features
    df['month'] = df.index.strftime('%m-%b')
    df['weekend'] = df.index.strftime('%w-%a')

    # derive the total sales
    df['sales_total'] = df.sale_amount * df.item_price

    return df


def get_sales_by_day(df):
    sales_by_day = df.resample('D')[['sales_total']].sum()
    sales_by_day['diff_with_last_day'] = sales_by_day.sales_total.diff()
    return sales_by_day