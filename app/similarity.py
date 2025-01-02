"""
Module contains machine learning functions to determine
similarity. Hosts a KNN model to find closest players.
"""

import os
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from .database.db_operations import get_player_info, get_player_name, query_all_master_table, query_all_players

FEATS = ['G', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FG%','FT%', 'TOV']

# deprecated for now
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
                'BLK': career_row.blocks,
                'FG%': career_row.fg_percentage,
                '3P%': career_row.three_point_percentage,
                'FT%': career_row.ft_percentage,
                'TOV':career_row.turnovers
            }
            
            player_data.append(career_dict)
    
    df = pd.DataFrame(player_data)
    return df
# slightly more optimized
def create_master_table2():
    master_players = query_all_master_table()
    columns = [
        'Player_ID', 'G', 'Pos', 'PTS', 'TRB', 'AST',
        'STL', 'BLK', 'TOV', 'FG%', '3P%',
        'FT%'
    ]
    
    data = []

    for player in master_players:
        data.append([
            player.player_id,
            player.games,
            player.pos,
            player.points,
            player.rebounds,
            player.assists,
            player.steals,
            player.blocks,
            player.turnovers,
            player.fg_percentage,
            player.three_point_percentage,
            player.free_throw_percentage,
        ])
    
    df = pd.DataFrame(data, columns=columns)
    return df

def scale_data(df):
    # adjust weights
    df['Pos'] = df['Pos']
    df['G'] = df['G'] * 0.25

    df['AST'] = df['AST'] * 1.4
    df['TRB'] = df['TRB'] * 1.2

    df['FG%'] = df['FG%'] * 0.75
    df['3P%'] = df['3P%'] * 0.75
    df['FT%'] = df['FT%'] * 0.25

    df['TOV'] = df['TOV'] * 0.5


    scaler = StandardScaler()
    df[FEATS] = scaler.fit_transform(df[FEATS])  # apply scaling
    
    return df


def closest_players_KNN(scaled_df, player_id, num_players):
    """Use KNN to find the most similar players"""
    # extract player data (excluding the 'Player_ID' and 'Pos')
    KNN_N = 5
    if num_players > 4: KNN_N = num_players + 1

    features = scaled_df[FEATS]

    knn = NearestNeighbors(n_neighbors=KNN_N, metric='euclidean')
    knn.fit(features)

    player_row = scaled_df[scaled_df['Player_ID'] == player_id]
    player_vector = player_row[FEATS]

    distances, indices = knn.kneighbors(player_vector)

    # distances[0] is list of all players (including self)
    similarity_scores = 1 / (1 + distances[0][1:num_players + 1])

    # get the closest players' data
    closest_players_index = indices[0][1:num_players + 1]
    closest_players = scaled_df.iloc[closest_players_index]['Player_ID']

    return closest_players, similarity_scores


def get_closest_player(id: int, num_players=3) -> str:
    """Returns the closest player by calling other functions"""
    try:
        scaled = scale_data(create_master_table2())
        # scaled = scale_data(create_master_table())
        
        closest_ids, scores = closest_players_KNN(scaled, id, num_players)
        closest_names = [get_player_name(player_id) for player_id in closest_ids]
        
        return closest_names, scores
    
    # sometimes KNN function returns value error, fix later
    except ValueError as e:
        print(f"ValueError: {e}")
        return [], []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return [], []


def sigmoid(x, k=10, c=0.30):
    return 1 / (1 + np.exp(-k * (x - c)))


def get_similarity_score(pid1: int, pid2: int) -> int:
    scaled_df = scale_data(create_master_table2())

    p1_row = scaled_df[scaled_df['Player_ID'] == pid1]
    p1_vector = p1_row[FEATS].values

    p2_row = scaled_df[scaled_df['Player_ID'] == pid2]
    p2_vector = p2_row[FEATS].values

    distance = np.linalg.norm(p1_vector - p2_vector)
    similarity_score = sigmoid(1 / (1 + distance))
    
    return similarity_score

import plotly.express as px

def get_kmeans_cluster(pid: int) -> int:
    try:
        df = create_master_table2()
        pid_col = df['Player_ID']

        feats = df.drop(['Player_ID'], axis=1)

        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(feats)

        kmeans = KMeans(n_clusters=4)

        feats['Player_ID'] = pid_col
        feats['Cluster'] = kmeans.fit_predict(df_scaled)
        feats['Name'] = feats['Player_ID'].apply(lambda x: get_player_name(x))

        generate_plotly(feats)

        cluster_num = int(feats[feats['Player_ID'] == pid]['Cluster'].values[0])
        return cluster_num

    except Exception as e:
        print(f"Error in get_kmeans_cluster: {e}")
        return -1  # Return a default value or handle it as needed


def generate_plotly(feats: int) -> None:
    fig = px.scatter(feats, x='PTS', y='AST', color='Cluster', hover_data=['TRB','Name'])
    fig.write_html('static/img/scatterplot.html')

    output_dir = 'static/img'
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, 'scatterplot.html')
    fig.write_html(output_file)
