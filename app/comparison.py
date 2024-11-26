import pandas as pd

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


