import pandas as pd
import numpy as np
from scipy.stats import kurtosis, skew


#beside getting the usual summary from describe function ,
#it adds the four more quantiles 5%, 1%,9%, 99% , for a comprehensive view of data at its tails


# THE FOLLOWING FUNCTION GETS THE WHOLE SUMMARY OF THE NUMERIC VARIABLES OF THE GIVEN DATAFRAME 

def get_whole_summary(df):

    #defining the quantiles at which we need to see data
    quant = [.05,.1,.9,.99]
    numeric_cols = []
    quant_names = []
    quant_num = []
    
    #creating the skew and kurtosis list 
    char_metrics = ['skew','kurtosis']
    skew_num = []
    skew_name = []
    kurt_num = []
    kurt_name = []

    #getting the summary of the data from the python function describe()
    #we will add the other information that we need to see into the summary object
    summary = df.describe()

    #collecting the list of numeric columns from the given dataframe
    for i in df.columns:
            if df[i].dtype != 'object':
                numeric_cols.append(i)

    #computing all the given quantiles (from given quant list) for all the numeric columns 
    for i in numeric_cols:
        for j in quant:
            quant_names.append(i + "_" + str(j))
            quant_num.append(np.quantile(df[i],j))

    #computing skew and kurtosis for all the numeric columns 
    for i in numeric_cols:
        skew_name.append( i + "_"+'skew')
        skew_num.append(skew(df[i]))
        kurt_name.append( i + "_"+'kurt')
        kurt_num.append(kurtosis(df[i]))

    #merging the name and num(value) lists into one for skew and kurtosis
    skew_name.extend(kurt_name)
    skew_num.extend(kurt_num)

    # adding the skew and kurtosis information into the quantile lists
    quant_num.extend(skew_num)
    quant_names.extend(skew_name)

    #transforming the lists for quantiles value and name into a dataframe
    quant_df = pd.DataFrame(quant_num, quant_names).reset_index()

    #renaming the columns
    quant_df.columns = ["variable","value"]

    #seperating the 'variable' columns to extract quantiles value
    quant_df[[" ","metric"]] = quant_df["variable"].str.rsplit("_",n = 1, expand = True)

    #dropping the redudant 'variable' column
    quant_df = quant_df.drop(["variable"],1)

    #pivoting the dataframe to match the summary dataframe 
    quant_df = quant_df.pivot(index="metric", columns = " ", values = "value").reset_index()

    #column-merging the summary and quantile dataframe
    sumamrized_df = pd.concat([summary,quant_df.set_index("metric")])

    #renaming the index
    sumamrized_df.index = ['count',  'mean',   'std',   'min', '25%',   '50%',   '75%',  'max',"5%",  "10%","90%",    "99%","skewness", "kurtosis"]

    #re-arranging the index for readability
    index_reorder = ['count',  'mean',   'std',   'min',"5%",  "10%",'25%', '50%',   '75%', "90%", "99%", 'max','skewness','kurtosis']
    sumamrized_df = sumamrized_df.reindex(index_reorder)

    return sumamrized_df




