# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 21:25:06 2024

@author: ckmim
"""


import pandas as pd


# Read CSV file into a Pandas DataFrame
file_path = r'D:/downloads/Brainstation Project/CSV Tables/campaign.xlsx'
df = pd.read_excel(file_path)

def preprocess_data(df):
    # Drop unnecessary column
    df = df.drop('Unnamed: 11', axis=1)
    
    # Convert 'launched' and 'deadline' to datetime objects
    df['launched'] = pd.to_datetime(df['launched'])
    df['deadline'] = pd.to_datetime(df['deadline'])
    
    # Calculate 'campaign_length'
    df['campaign_length'] = (df['deadline'] - df['launched']).dt.days
    
    return df
# Preprocess data
df = preprocess_data(df)

def filter_by_criteria(df, country_id, sub_category_id=None):
    if sub_category_id is None:
        return df[df['country_id'] == country_id]
    else:
        return df[(df['country_id'] == country_id) & (df['sub_category_id'] == sub_category_id)]

# Filter for USA campaigns
us_df = filter_by_criteria(df, 2, None )

# Filter for campaigns w/tabletop games & USA
us_ttgame_df = filter_by_criteria(df, 2, 14)

us_df.loc[:, 'campaign_length_qtrs'] = pd.qcut(us_df['campaign_length'], q=4, labels=False, duplicates='drop')

us_ttgame_df.loc[:, 'campaign_length_qtrs'] = pd.qcut(us_df['campaign_length'], q=4, labels=False,duplicates='drop') 

#The algo is not able to find the quartiles given the numbers. 

def calc_quartiles_thirds(df):
    df.loc[:, 'campaign_length_third'] = pd.qcut(df['campaign_length'], q=3, labels=False)
    df.loc[:,'campaign_length_quartile'] = pd.qcut(df['campaign_length'].rank(method='first'), q=[0, 0.25, 0.5, 0.75, 1], labels=False)
    return df

# Calculate quartiles and thirds
us_df = calc_quartiles_thirds(us_df)
us_ttgame_df = calc_quartiles_thirds(us_ttgame_df)

def calc_grouped_stats(df, grouping_column):
    return df.groupby(grouping_column)['pledged'].agg(['sum', 'describe'])


# Calculate grouped statistics
us_tt_gggrouped_quartile = calc_grouped_stats(us_ttgame_df, 'campaign_length_quartile')
us_tt_ggrouped_third = calc_grouped_stats(us_ttgame_df, 'campaign_length_third')

us_grouped_quartile = calc_grouped_stats(us_df, 'campaign_length_quartile')
us_grouped_third = calc_grouped_stats(us_df, 'campaign_length_third')

