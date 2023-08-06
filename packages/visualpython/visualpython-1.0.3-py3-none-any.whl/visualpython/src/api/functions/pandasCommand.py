"""
Pandas Objects Command
"""

def _vp_get_variables_list(types):
    """
    Get Variable list in types
    """
    notUsingVariables = ['_html', '_nms', 'NamespaceMagics', '_Jupyter', 'In', 'Out', 'exit', 'quit', 'get_ipython']
    notUsingTypes = ['module', 'function', 'builtin_function_or_method', 'instance', '_Feature', 'type', 'ufunc']

    varList = []
    searchList = globals()
    if (type(types) == list) and (len(types) > 0):
        varList = [{'varName': v, 'varType': type(eval(v)).__name__} for v in searchList if (not v.startswith('_')) & (v not in notUsingVariables) & (type(eval(v)).__name__ in types)]
    else:
        varList = [{'varName': v, 'varType': type(eval(v)).__name__} for v in searchList if (not v.startswith('_')) & (v not in notUsingVariables) & (type(eval(v)).__name__ not in notUsingTypes)]

    return varList

def _vp_get_rows_list(df):
    """
    Get Rows List with Detail Information
    """
    rowList = []
    indexType = str(df.index.dtype)
    for i, r in enumerate(df.index):
        rInfo = { 'label': r, 'value': r, 'location': i }
        # value
        if type(r).__name__ == 'str':
            rInfo['value'] = "'{}'".format(r)
            rInfo['index_dtype'] = indexType # object
        elif type(r).__name__ == 'Timestamp':
            rInfo['label'] = str(r)
            rInfo['value'] = "'{}'".format(r)
            rInfo['index_dtype'] = indexType # datetime64[ns] TODO: exception consideration needed
        rowList.append(rInfo)
    return rowList

def _vp_get_columns_list(df):
    """
    Get Columns List with Detail Information
    """
    colList = []
    for i, c in enumerate(df.columns):
        cInfo = { 'label': c, 'value': c, 'dtype': str(df[c].dtype), 'array': str(df[c].array), 'location': i }
        # value
        if type(c).__name__ == 'str':
            cInfo['value'] = "'{}'".format(c)
        elif type(r).__name__ == 'Timestamp':
            cInfo['value'] = str(c)
        # category - iopub data rate limit issue...
        if str(df[c].dtype) == 'object':
            uniqValues = df[c].dropna().unique()
            if len(uniqValues) <= 20:
                cInfo['category'] = [{ "value": "'{}'".format(u) if type(u) == str else u, "label": u } for u in uniqValues]
            else:
                cInfo['category'] = []
        else:
            cInfo['category'] = []
        colList.append(cInfo)
    return colList

def _vp_get_column_category(df, col):
    """
    Get Column's Uniq values(Categrical data only, limit 20)
    """
    uniqValues = df[col].dropna().unique()
    category = []
    if len(uniqValues) <= 20:
        category = [{ "value": "{}".format(u) if type(u) == str else u, "label": u } for u in uniqValues]
    return category

def _vp_get_dataframe_as_list(df):
    """
    Get Dataframe as List
    """
    return df.values.tolist()