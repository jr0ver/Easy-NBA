"""
Module for handling player data when first initializing and
using the app. Retrieves player information by calling functions
from DB module and accessing various fields
"""

from .data_cleaning import front_end_clean
from .database.db_operations import add_player, convert_reg_to_df, convert_post_to_df, delete_player_from_id, get_player_info, get_player_name, get_player_object, get_player_tables
from .models.BasketballReference import BasketballReference
from .database.data_retrieval import PlayerInfo
from .similarity import get_closest_player


def handle_player_data(user_input) -> tuple:
    player_lower = user_input.lower()
    player_obj = get_player_object(player_lower)

    # player already in DB, READ
    if player_obj:
        print("Player is already in the database")
        reg_query, playoffs_query = get_player_tables(player_obj)
        reg, playoffs = convert_reg_to_df(reg_query), convert_post_to_df(playoffs_query)
        player_info = get_player_info(player_lower)
    
    # player not in DB, WRITE
    elif not player_obj:
        try:
            player_cleaned = user_input.replace("'", "").lower().split()
            player_cleaned = player_cleaned[0] + "_" + player_cleaned[1]
            player_raw = BasketballReference(user_input)
            player = PlayerInfo(player_raw)
            reg, playoffs = player.reg, player.post
            player_info = player.get_player_info()

            # print("FINAL", reg)
            
            if not player_obj:
                print("Player is NEW")
                add_player(player_lower, reg, playoffs, player_info)
                player_obj = get_player_object(player_lower)
            
            
        except Exception as e:
            print("Sorry, the player couldn't be found:", e)
            return None
    
    reg, playoffs = front_end_clean(reg), front_end_clean(playoffs)
    return player_obj, reg, playoffs, player_info

def handle_closest_player(id: int) -> str:
    if id is None:
        return None
    # return get_closest_player(id)
    return "Oops! There has been an error calculating the closest player."

def handle_deletion_status(id: int) -> list[str, bool]:
    p_name = get_player_name(id)
    return [p_name, delete_player_from_id(id)]