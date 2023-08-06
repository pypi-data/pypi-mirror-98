import pandas as pd
import numpy as np
import re
#pattern = re.compile("^([A-Z][0-9]+)+$")
#pattern.match(string)

def ensure_list(variable):
    if not isinstance(variable, list):
        variable = [variable]
    return variable

def read_spreadsheet(path):
    try:
        df = pd.read_excel(path)
        filetype = 'EXCEL'
    except Exception:
        df = pd.read_csv(path)
        filetype = 'CSV'
    return df, filetype

def write_spreadsheet(data,path):
    pattern = re.compile('.*\.csv$')
    if re.compile('.*\.csv$').search(path):
        data.to_csv(path, index = False)
    elif re.compile('.*\.xlsx$').search(path):
        data.to_excel(path, index = False)
    return 0
    

def df_difference(data, subtract_df):
    """
    Dataframe difference, returns all rows in data that are not in subtract dataframe
    ---inputs---
    data - pandas data frame
    subtract_df - pandas data frame to be subtracted from data; has a same schema as data.
    """
    return data[~data.fillna(0).apply(tuple,1).isin(subtract_df.fillna(0).apply(tuple,1))]

def union(dfs_list: list):
    return pd.concat(dfs_list)


def sort(data, col_names, ascending = True):
    """
    sort pandas dataframe based on columns provided in column_names (str or list) in order based on ascending param (str or list)
    """
    return data.sort_values(by = col_names, ascending = ascending)

def melt(data, id_vars = None, value_vars = None, variable_name = None, value_name = 'value'):
    return data.melt(id_vars = id_vars, value_vars = value_vars, var_name = variable_name, value_name = value_name)

def dcast(data, value_variable = None, index = None, columns = None, fun_aggregate = np.mean, fill_value = None):
    if fun_aggregate is None:
        out = data.pivot(index = index, columns = columns, values = value_variable)
        if fill_value is not None:
            out.fillna(fill_value, inplace = True)
    else:
        out = data.pivot_table(values = value_variable, index = index, columns = columns, aggfunc = fun_aggregate, fill_value = fill_value, dropna = False)
    return out#.pivot_table(values = value_variable, index = index, columns = columns, aggfunc = fun_aggregate, fill_value = fill_value, dropna = False)

def find_value(data, value, search_cols = None, match = 'exact'):
    if search_cols is None:
        search_cols = data.columns
    else: search_cols = ensure_list(search_cols)
    dict_cols = dict(zip(search_cols, range(len(search_cols))))
    stack = data.rename(columns = dict_cols).stack()
    if match == 'pattern':
        out = stack[stack.astype('str').str.contains(value)].index.to_list()
    else:
        out = stack[stack == value].index.to_list()
    return out
    
def find_replace(data, pattern:str, replacement:str, search_cols = None, match = 'exact'):
    data = data.copy()
    if search_cols is None:
        search_cols = data.columns
    else: search_cols = ensure_list(search_cols)
    dict_cols = dict(zip(search_cols, range(len(search_cols))))
    #old_columns = data.columns
    old_dtypes = data.dtypes
    stack = data.rename(columns = dict_cols)[[dict_cols[i] for i in dict_cols]].stack()
    if match == 'pattern':
        out = stack.astype('str').str.replace(pattern, replacement).unstack()
    else:
        out = stack.astype('str').replace(pattern, replacement).unstack()
    data[[i for i in dict_cols]] = out
    for i in dict_cols:
        try:
            data[i] = data[i].astype(old_dtypes[i])
        except:
            pass
            
    return data