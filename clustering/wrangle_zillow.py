#Functions of the work above needed to aquire and prepare
#a new sample of data

import acquire
import prepare

def wrangle_zillow_data():
    df = acquire_zillow()
    df = zillow_single_unit(df)
    df = remove_columns(df,['calculatedbathnbr','finishedsquarefeet12',\
        'fullbathcnt','propertycountylandusecode','unitcnt','structuretaxvaluedollarcnt',\
        'landtaxvaluedollarcnt','assessmentyear','propertyzoningdesc'])
    df = handle_missing_values(df)
    df.dropna(inplace = True)
    return df