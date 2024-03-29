import pandas as pd
import numpy as np


# gets the unique values from a pandas data frame for each column if its level is smaller than the given number 

def get_unique_values(df, n) : 
    for i in df.columns:
        if df[i].dtype == 'object':
            if len(df[i].unique()) < n:
                print(len(df[i].unique()),"unique values for", i,":",'\n',df[i].unique(), '\n')
            elif len(df[i].unique()) >= n:
                print(len(df[i].unique()),"unique values for", i, "(greater than",n,")",'\n' )
