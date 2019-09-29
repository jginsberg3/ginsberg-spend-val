import pandas as pd
from typing import Tuple


def check_file(file: str) -> Tuple[bool, str]:
    '''
    Return True if file passes QA, False if not.
    File should match formatting requirements for uploading to Redshift.
    '''
    if file.split('.')[1] in ['csv']:
        df = pd.read_csv(file)
    if file.split('.')[1] in ['xls', 'xlsx']:
        df = pd.read_excel(file)
        
    
    # do cols match exactly?
    correct_cols = ['date', 'placementid', 'placement', 'spend']
    df_cols = [col.strip().replace('_', '').replace('-', '').lower() for col in df.columns]
    if df_cols != correct_cols:
        return (False, 'Check that column names and order match:  date, placment_id, placement, spend.  Also make sure there are no additional columns.')

    # are there many empty rows?
    if len(df.dropna()) < len(df) - 5:
        return (False, 'Check that there are not many empty rows in the file')

    # are data types correct? ("-" char in spend col)
    d_types = {'spend': float}
    for _col, _type in d_types.items():
        try:
            df[_col].astype(_type)
        except:
            return (False, 'Check that data types are correct.  For example, no "-" characters in the spend column.')

    return (True, 'File format is good.')
