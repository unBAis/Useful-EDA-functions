
#THE FOLLOWING FUNCTION GETS THE SKEWNESS AND KURTOSIS FOR MULTIPLE SUBSETS FOR THE GIVEN DATA

def get_skew_kurt_for_subset(df, req_col, bot_q = [.01,.03,.05,.10,.13,.15,.20,.25,.30,.35,.40,.50]):

    # df = data
    #req_col = a list of numeric columns 
    # bot_q = a list of quantiles for which data needs to be truncated from the bottom and get the skewness and kurtosis
    # an another list ,top_q will get created from bot_q which is 1-bot_q, its a list of top quantiles for which data will be truncated 
    # from top to get skewness and kurtosis for the truncated data

    #creating the list for top quantiles from the given bottom quantiles 
    top_q = []
    for i in bot_q:
        top_q.append(1-i)
    
    sk_lst = []

    #computing the skew and kurtosis for each column after removing a gven quantile from both tail for all quantiles  
    for col in req_col: 
        
        #creating the list for top and bottom quantiles for the given columns (req_col)
        bot_num_q = []
        top_num_q = []
        for i in bot_q:
            bot_num_q.append(np.quantile(df[col],i))
        for i in top_q:
            top_num_q.append(np.quantile(df[col],i))
    
        #creating the list for skew and kurtosis for the given columns (req_col) after removing top and corresponding bottom quantile for all the quantiles one at a time
        skew_lst = []
        kurt_lst = []
        for i, j in zip(top_num_q,bot_num_q):
            skew_lst.append(skew(df[(df[col] < i ) & (df[col] > j)][col]))
            kurt_lst.append(kurtosis(df[(df[col] < i ) & (df[col] > j)][col]))

        #creating the dataframe  
        sk_df = pd.DataFrame({'bottom_quantile': bot_q, 'top_quantile': top_q, 'skewness': skew_lst, 'kurtosis' : kurt_lst })
    
        #creating a column called 'variable' with value as the column name for which its getting run 
        sk_df['variable'] = col

        #labeling the tail at which we computed the skew and kurtosis 
        sk_df['tail'] = 'two_tail'

        #adding it to the list sk_lst
        sk_lst.append(sk_df)


    #computing the skew and kurtosis for each column after removing a gven quantile from right tail for all quantiles

    #the process is same as two tail except for the fact we only remove the quantile data from top quantile (right tail)
    for col in req_col:
                
        bot_num_q = []
        top_num_q = []
        for i in bot_q:
            bot_num_q.append(np.quantile(df[col],i))
        for i in top_q:
            top_num_q.append(np.quantile(df[col],i))
         
        skew_lst = []
        kurt_lst = []
        for i in top_num_q:
            skew_lst.append(skew(df[(df[col] < i ) ][col]))
            kurt_lst.append(kurtosis(df[(df[col] < i )][col]))
        sk_df = pd.DataFrame({ 'top_quantile': top_q, 'skewness': skew_lst, 'kurtosis' : kurt_lst })
        
        sk_df['variable'] = col
        sk_df['tail'] = 'right_tail'
        sk_df['bottom_quantile'] = None
        sk_lst.append(sk_df) 
   
    #computing the skew and kurtosis for each column after removing a gven quantile from right tail for all quantiles

    #the process is same as two tail except for the fact we only remove the quantile data from bottom quantile (bottom tail)
    for col in req_col: 
                
        bot_num_q = []
        top_num_q = []
        for i in bot_q:
            bot_num_q.append(np.quantile(df[col],i))
        for i in top_q:
            top_num_q.append(np.quantile(df[col],i))
        
        skew_lst = []
        kurt_lst = []
        for i in bot_num_q:
            skew_lst.append(skew(df[(df[col] > i ) ][col]))
            kurt_lst.append(kurtosis(df[(df[col] > i )][col]))
        sk_df = pd.DataFrame({'bottom_quantile': bot_q, 'skewness': skew_lst, 'kurtosis' : kurt_lst })
        
        sk_df['variable'] = col
        sk_df['tail'] = 'left_tail'
        sk_df['top_quantile'] = None
        sk_lst.append(sk_df)        

    #merging all the dataframes in sk_lst (both tail, right tail, left tail)
    skew_kurt_df = pd.concat(sk_lst).reset_index(drop = True)

    #re-ordering the columns 
    skew_kurt_df = skew_kurt_df[['tail','variable','top_quantile','bottom_quantile','skewness','kurtosis']]
    
    return(skew_kurt_df)
