import pandas as pd
import env

def get_db_url(database_name):
    return f'mysql+pymysql://{env.user}:{env.password}@{env.host}/{database_name}'

# Function that acquires zillow data from 2017 with no null latitude and longitude values,
# and no duplicate property id's

def acquire_zillow():
    query = '''
    SELECT logerror, transactiondate, properties_2017.*, airconditioningtype.`airconditioningdesc`, `architecturalstyletype`.`architecturalstyledesc`, `buildingclasstype`.buildingclassdesc, `heatingorsystemtype`.`heatingorsystemdesc`, propertylandusetype.`propertylandusedesc`, `storytype`.`storydesc`, `typeconstructiontype`.`typeconstructiondesc` FROM predictions_2017

	JOIN
        (SELECT pred_17.parcelid, Max(transactiondate) as tdate 
        FROM predictions_2017 as pred_17
        GROUP BY pred_17.parcelid ) as sub
    ON (sub.parcelid = predictions_2017.parcelid and sub.tdate = predictions_2017.transactiondate)
    
	LEFT JOIN `properties_2017` ON sub.parcelid = properties_2017.parcelid
	LEFT JOIN `airconditioningtype` USING(`airconditioningtypeid`)
	LEFT JOIN `architecturalstyletype` USING(`architecturalstyletypeid`)
	LEFT JOIN `buildingclasstype` USING(`buildingclasstypeid`)
	LEFT JOIN `heatingorsystemtype` USING(`heatingorsystemtypeid`)
	LEFT JOIN `propertylandusetype` USING(`propertylandusetypeid`)
	LEFT JOIN `storytype` USING(`storytypeid`)
	LEFT JOIN `typeconstructiontype` USING(`typeconstructiontypeid`)
	WHERE (`properties_2017`.`latitude` IS NOT NULL AND `properties_2017`.longitude IS NOT NULL);
    '''
    df = pd.read_sql(query, get_db_url('zillow'))
    return df  

# function that summarizes the dataframe data into a 
# sample view, datatypes, value counts, summary stats, ...)

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

# Function that write a function that takes in a dataframe of observations
# and attributes and returns a df where each row is an atttribute name, 
# the first column is the number of rows with missing values for that attribute, 
# and the second column is percent of total rows that have missing values for that attribute. 
# Run the function and document takeaways from this on how you want to handle missing values.

# Take in a dataframe and returns a dataframe with the number of rows and percent of rows with missing values for each column.

def nulls_by_col(df):
    num_missing = df.isnull().sum()
    rows = df.shape[0]
    pct_missing = num_missing/rows
    cols_missing = pd.DataFrame({'num_rows_missing': num_missing, 'pct_rows_missing': pct_missing})
    return cols_missing

def print_nulls_by_column(df):
    print('--- Nulls By Column')
    print(nulls_by_col(df))

# Function that takes in a dataframe and returns a dataframe 
# with 3 columns: the number of columns missing, percent of columns missing, 
# number of rows with n columns missing. 

# Function from summarize.py that takes in a dataframe and returns a dataframe with 3 columns:  
#    - the number of columns missing
#    - percent of columns missing
#    - number of rows with n columns missing

def nulls_by_row(df):
    num_cols_missing = df.isnull().sum(axis=1)
    pct_cols_missing = df.isnull().sum(axis=1)/df.shape[1]*100
    rows_missing = pd.DataFrame({'num_cols_missing': num_cols_missing, 'pct_cols_missing': pct_cols_missing}) \
    .reset_index().groupby(['num_cols_missing','pct_cols_missing']).count().rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return rows_missing

def print_nulls_by_row(df):
    print('--- Nulls By Row')
    print(nulls_by_row(df))