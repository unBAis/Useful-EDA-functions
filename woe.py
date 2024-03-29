import pandas as pd
import numpy as np


#gets the weight of evidence and information value for each column given in the function and return the Dataframe for the same with added information
# the arguments for the function are defined as follows: 
#df = data 
#num_cols = list of numeric/integer columns
#char_cols = list of character columns
#quantile_group = an integer for how many groups are intended for numeric/interger columns distribution
#target = the binary column for which woe needs to be calculated 

def get_woe_df(df, num_cols, char_cols,quantile_group ,target):
    num_lst = []
    char_lst = []
    bin_col_names = []
    
    for i in num_cols:
         bin_col_names.append('bin_'+ i)

    for i,j in zip(num_cols,bin_col_names):
        df[j] = pd.qcut(df[i], q=quantile_group , precision = 0)

        for a in range(df[j].nunique()):
            num_val = list(df[j].unique())[a]
            num_lst.append({
                'Variable': j,
                'Value': num_val,
                'All': df[df[j] == num_val].count()[j],
                'Good': df[(df[j] == num_val) & (df[target] == 0)].count()[j],
                'Bad': df[(df[j] == num_val) & (df[target] == 1)].count()[j]
            })
        num_df = pd.DataFrame(num_lst)

    for k in char_cols:  
        for b in range(df[k].nunique()):
            char_val = list(df[k].unique())[b]
            char_lst.append({
                'Variable': k,
                'Value': char_val,
                'All': df[df[k] == char_val].count()[k],
                'Good': df[(df[k] == char_val) & (df[target] == 0)].count()[k],
                'Bad': df[(df[k] == char_val) & (df[target] == 1)].count()[k]
            })   
        char_df = pd.DataFrame(char_lst)

    woe_df = pd.concat([char_df,num_df])
    woe_df['Distr_Good'] = woe_df['Good'] / woe_df['Good'].sum()
    woe_df['Distr_Bad'] = woe_df['Bad'] / woe_df['Bad'].sum()
    woe_df['WoE'] = np.log(woe_df['Distr_Good'] / woe_df['Distr_Bad'])
    woe_df = woe_df.replace({'WoE': {np.inf: 0, -np.inf: 0}})
    woe_df['IV'] = (woe_df['Distr_Good'] - woe_df['Distr_Bad'])*woe_df['WoE']
    iv = woe_df['IV'].sum()

    woe_df = woe_df.sort_values(by=['Variable','WoE'],ascending = False).reset_index(drop = True)
    IV_df = woe_df.groupby('Variable').agg(Variable_IV = ('IV','sum')).reset_index()
    woe_df = woe_df.merge(IV_df, on = 'Variable', how= 'left')

    return woe_df
