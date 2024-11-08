from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from database import get_player_info, get_player_name, query_all_players

def create_master_table():
    players = query_all_players()
    
    player_data = []
    
    pos_mapping = {
        'PG': 1,
        'SG': 2,
        'SF': 3,
        'PF': 4,
        'C': 5
    }
    
    for p in players:
        career_row = next((row for row in p.reg_stats if row.season == 'Career'), None)
        
        if career_row:
            info = get_player_info(p.name)
            pos = info.get('position')[0]
            
            pos_num = pos_mapping.get(pos)  # convert position to a numeric value

            career_dict = {
                'Player_ID': p.id,
                'Pos': pos_num, 
                'G': career_row.games,
                'PTS': career_row.points,
                'TRB': career_row.rebounds,
                'AST': career_row.assists,
                'STL': career_row.steals,
                'BLK': career_row.blocks
            }
            
            player_data.append(career_dict)
    
    df = pd.DataFrame(player_data)
    return df

def scale_data(df):
    columns_to_scale = ['G', 'PTS', 'TRB', 'AST', 'STL', 'BLK']
    
    scaler = StandardScaler()
    df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])  # apply scaling
    
    return df


def closest_player_KNN(scaled_df, player_id):
    """Use KNN to find the most similar player"""
    # extract player data (excluding the 'Player_ID' and 'Pos')
    KNN_N = 5
    features = scaled_df[['G', 'PTS', 'TRB', 'AST', 'STL', 'BLK']]

    knn = NearestNeighbors(n_neighbors=KNN_N, metric='euclidean')
    knn.fit(features)

    player_row = scaled_df[scaled_df['Player_ID'] == player_id]
    player_vector = player_row[['G', 'PTS', 'TRB', 'AST', 'STL', 'BLK']]

    distances, indices = knn.kneighbors(player_vector)

    # get the closest player's data
    closest_player_index = indices[0][1] 
    closest_player = scaled_df.iloc[closest_player_index]['Player_ID']

    return closest_player

def get_closest_player(id: int) -> str:
    """Returns the closest player name to player with given id."""
    try:
        scaled = scale_data(create_master_table())
        closest = closest_player_KNN(scaled, id)
        closest_name = get_player_name(closest)
        return closest_name
    
    # sometimes KNN function returns value error, fix later
    except ValueError as e:
        print(f"ValueError: {e}")
        return "Error: Could not find closest player."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error: An unexpected issue occurred."
