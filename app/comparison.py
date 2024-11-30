import pandas as pd

def safe_float(value):
    # this function handles the case where the value is '-' and returns 0 instead
    return float(value) if value != '-' else 0.0

def create_comp_df(reg: pd.DataFrame, post: pd.DataFrame) -> pd.DataFrame:
    reg = reg.copy()
    reg['Season'] = 'Regular'
    
    if not post.empty:
        post = post.copy()
        post['Season'] = 'Playoffs'
    else:
        columns = ['Season', 'Team', 'Pos', 'G', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%']
        post = pd.DataFrame([['Playoffs', '0 Yrs', '-', '-', '-', '-', '-', '-', '-', '-']], columns=columns)
    
    comp_df = pd.concat([reg, post], ignore_index=True)
    comp_df.drop(['Pos'], axis=1, inplace=True)
    comp_df.rename(columns={'Team': 'Length'}, inplace=True)
    
    return comp_df

def create_comp_dict(comp_df1: pd.DataFrame, comp_df2: pd.DataFrame) -> tuple[dict,dict]:
    if comp_df1 is not None and comp_df2 is not None:
        player1_regular = comp_df1[comp_df1['Season'] == 'Regular'].iloc[0]
        player2_regular = comp_df2[comp_df2['Season'] == 'Regular'].iloc[0]

        player1_stats = {
            "PTS": float(player1_regular['PTS']),
            "TRB": float(player1_regular['TRB']),
            "AST": float(player1_regular['AST']),
            "BLK": safe_float(player1_regular['BLK']),
            "STL": safe_float(player1_regular['STL']),
            "FG%": (player1_regular['FG%'])
        }
        player2_stats = {
            "PTS": float(player2_regular['PTS']),
            "TRB": float(player2_regular['TRB']),
            "AST": float(player2_regular['AST']),
            "BLK": safe_float(player2_regular['BLK']),
            "STL": safe_float(player2_regular['STL']),
            "FG%": (player2_regular['FG%'])
        }

        return player1_stats, player2_stats
    
    return {}, {}


