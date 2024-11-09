from data_cleaning import front_end_clean
from database import add_player, convert_reg_to_df, convert_post_to_df, get_player_info, get_player_object, get_player_tables
from BasketballReference import BasketballReference
from data_retrieval import PlayerInfo
# from similarity import get_closest_player

def handle_player_data(user_input):
    player_lower = user_input.lower()
    player_obj = get_player_object(player_lower)

    # player already in DB, READ
    if player_obj:
        print("Player is already in the database")
        reg_query, playoffs_query = get_player_tables(player_obj)
        reg, playoffs = convert_reg_to_df(reg_query), convert_post_to_df(playoffs_query)
        player_info = get_player_info(player_lower)
    
    # player not in DB, WRITE
    else:
        print("Player is NEW")
        try:
            player_cleaned = user_input.replace("'", "").lower().split()
            player_cleaned = player_cleaned[0] + "_" + player_cleaned[1]
            player_raw = BasketballReference(user_input)
            player = PlayerInfo(player_raw)
            reg, playoffs = player.reg, player.post
            player_info = player.get_player_info()

            add_player(player_lower, reg, playoffs, player_info)
            player_obj = get_player_object(player_lower)
        
        except Exception as e:
            print("Sorry, the player couldn't be found:", e)
            return None

    return player_obj, reg, playoffs, player_info
