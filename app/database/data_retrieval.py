"""
Module retrieves the various scraped data and packages it into
a PlayerInfo object.
"""

import pandas as pd
from bs4 import BeautifulSoup
from ..models.BasketballReference import BasketballReference
from ..awards import (
    format_all_league,
    get_all_league_list,
    get_awards_list,
    seperate_all_league,
)
from ..data_cleaning import clean_table


class PlayerInfo:
    def __init__(self, player_ref: BasketballReference):
        self.player_ref = player_ref
        self.reg = clean_table(self.player_ref.get_regular_season_stats())
        self.post = clean_table(self.player_ref.get_playoff_stats())

    # def get_primary_teams(self):
    #     teams = (self.reg['Team'] != "-")['Team'].value_counts()
    #     print(teams)

    def get_teams(self):
        relevant_rows = self.reg.iloc[: self.reg.index.get_loc("TOT_1")]
        teams = relevant_rows["Team"].value_counts().index.tolist()
        filtered_teams = [team for team in teams if team not in ["2TM", "3TM", "-"]]
        if len(filtered_teams) > 3:
            return filtered_teams[:3]
        return filtered_teams

    def get_position(self):
        relevant_rows = self.reg.iloc[: self.reg.index.get_loc("TOT_1")]
        positions = relevant_rows["Pos"].value_counts()

        top_position = positions.index[0]

        if len(positions) > 1 and positions.iloc[1] >= positions.iloc[0] * 0.33:
            return [top_position, positions.index[1]]
        return [top_position]

    def get_player_info(self) -> dict[str]:
        """arranges the player_info dictionary for the app_route"""

        # awards require info from 2 places
        awards = get_awards_list(self.player_ref.get_player_div())
        extras = seperate_all_league(get_all_league_list(self.player_ref.soup))
        extras = format_all_league(extras)
        if extras:
            awards.extend(extras)

        player_info = {
            "player_name": self.player_ref.name,
            "img_link": self.player_ref.get_br_img(),
            "position": self.get_position(),
            "teams": self.get_teams(),
            "awards": awards,
        }
        return player_info
