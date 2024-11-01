from models import db, Player, RegularSeason, PostSeason
import pandas as pd

def add_player(player_query, reg, playoffs):
    "Writes a new player to the DB"
    try:
        new_player = Player(name=player_query)
        db.session.add(new_player)
        db.session.commit()

        for index in range(len(reg)):
            reg_season_entry = RegularSeason(
                player_id=new_player.id,
                season=reg.iloc[index]['Season'],
                team=reg.iloc[index]['Team'],
                pos=reg.iloc[index]['Pos'],
                games=int(reg.iloc[index]['G']),
                points=reg.iloc[index]['PTS'],
                rebounds=reg.iloc[index]['TRB'],
                assists=reg.iloc[index]['AST'],
                steals=reg.iloc[index]['STL'],
                blocks=reg.iloc[index]['BLK']
            )
            db.session.add(reg_season_entry)

        for index in range(len(playoffs)):
            post_season_entry = PostSeason(
                player_id=new_player.id,
                season=playoffs.iloc[index]['Season'],
                team=playoffs.iloc[index]['Team'],
                pos=playoffs.iloc[index]['Pos'],
                games=int(playoffs.iloc[index]['G']),
                points=playoffs.iloc[index]['PTS'],
                rebounds=playoffs.iloc[index]['TRB'],
                assists=playoffs.iloc[index]['AST'],
                steals=playoffs.iloc[index]['STL'],
                blocks=playoffs.iloc[index]['BLK']
            )
            db.session.add(post_season_entry)

        db.session.commit()

    except Exception as e:
        print("Error adding player:", e)
        return None

def get_player_data(player_query):
    """Given a player name queries for it in the DB"""
    try:
        query = Player.query.filter_by(name=player_query).first()
        if query:
            reg_query = RegularSeason.query.filter_by(player_id=query.id).all()
            playoffs_query = PostSeason.query.filter_by(player_id=query.id).all()
            return reg_query, playoffs_query
        return None, None
    except Exception as e:
        print("Error retrieving player data:", e)
        return None, None

def adjust_read_df_index(df: pd.DataFrame):
    if df is None or df.empty:
        return df
    career_index = df[df['Season'] == 'Career'].index[0]
    new_index = list(range(career_index))  # Original indices before "Career"

    for i in range(career_index, len(df)):
        new_index.append(f'TOT_{i - career_index + 1}')

    df.index = new_index
    return df


def convert_to_dataframe(reg_query, playoffs_query):
    """Converts SQL tables to viewable pandas DFs"""
    try:
        reg_data = [{
            'ID': season.id,
            'Season': season.season,
            'Team': season.team,
            'Pos': season.pos,
            'G': season.games,
            'PTS': season.points,
            'TRB': season.rebounds,
            'AST': season.assists,
            'STL': season.steals,
            'BLK': season.blocks
        } for season in reg_query]

        reg_df = pd.DataFrame(reg_data)

        # sort the DataFrame by ID and reset index
        reg_df.sort_values(by='ID', inplace=True)
        reg_df.reset_index(drop=True, inplace=True)
        reg_df.drop(['ID'], axis=1, inplace=True)

        # print("REGULAR SEASON DF:", reg_df)

        if playoffs_query:
            playoffs_data = [{
                'ID': playoff.id,
                'Season': playoff.season,
                'Team': playoff.team,
                'Pos': playoff.pos,
                'G': playoff.games,
                'PTS': playoff.points,
                'TRB': playoff.rebounds,
                'AST': playoff.assists,
                'STL': playoff.steals,
                'BLK': playoff.blocks
            } for playoff in playoffs_query]

            playoffs_df = pd.DataFrame(playoffs_data)

            # sort the playoffs DataFrame by ID and reset index
            playoffs_df.sort_values(by='ID', inplace=True)
            playoffs_df.reset_index(drop=True, inplace=True)
            playoffs_df.drop(['ID'], axis=1, inplace=True)
        else:
            playoffs_df = pd.DataFrame(columns=['Season', 'Team', 'Pos', 'G', 'PTS', 'TRB', 'AST', 'STL', 'BLK'])

        # print("PLAYOFFS DF:", playoffs_df)

        return adjust_read_df_index(reg_df), adjust_read_df_index(playoffs_df)
    
    except Exception as e:
        print("Error converting to DataFrame:", e)
        return None, None