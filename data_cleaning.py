import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

def convert_type(df):
    # define the numerical columns you want to convert
    numerical_columns = ["G", "PTS", "TRB", "AST", "STL", "BLK"]
    # df = df.copy()
    
    for col in numerical_columns:
        if col in df.columns:  # check if the column exists
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def clean_aggregates(df: pd.DataFrame):
    # create boolean Series
    has_yrs = df['Season'].str.contains('Yr', case=False)
    yrs_indices = df[has_yrs].index.tolist()
    agg_count = 1

    for i in yrs_indices:
        # entire career case
        if '(' not in df.at[i, 'Season']:
            df.at[i, 'Season'] = 'Career'
        # one team case
        else:
            team = df.at[i, 'Season']
            pos = team.find('(')
            df.at[i, 'Season'] = team[:pos]
            df.at[i, 'Team'] = np.nan

        df.rename(index={i: f"TOT_{agg_count}"}, inplace=True)
        agg_count += 1
    
def clean_fill(df: pd.DataFrame):
    df.replace(r"^Did not play.*", "-", regex=True, inplace=True)
    df.fillna(-1, inplace=True)
    df['G'] = df['G'].astype(int)
    
def clean_table(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return df # must fix later
     
    df = convert_type(df)

    columns_to_drop = ['Age', 'Lg', 'GS','MP', 'FGA', 'FG', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 
                   'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TOV', 'PF', 'Awards']

    existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    df = df.drop(existing_columns_to_drop, axis=1)

    df = df.dropna(axis=0, how='all')
    df.index = range(1, len(df) + 1)
    clean_aggregates(df)
    clean_fill(df)
    return df
