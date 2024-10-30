import pandas as pd
from bs4 import BeautifulSoup
from BasketballReference import BasketballReference
from data_cleaning import clean_table


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

        if len(teams) > 3:
            return teams[:3]
        return teams

    def get_position(self):
        relevant_rows = self.reg.iloc[: self.reg.index.get_loc("TOT_1")]
        positions = relevant_rows["Pos"].value_counts()

        top_position = positions.index[0]

        if len(positions) > 1 and positions.iloc[1] >= positions.iloc[0] * 0.33:
            return [top_position, positions.index[1]]
        return [top_position]

    def get_player_info(self) -> dict[str]:
        """Given a player, the function calls functions from the modules
        land_of_bball.py and bbal_ref.py to sequentially obtain and produce
        a dictionary of various player information
        """
        player_info = {
            "player_name": self.player_ref.name,
            "img_link": self.player_ref.get_br_img(),
            "position": self.get_position(),
            "teams": self.get_teams(),
        }
        # show_graph(reg)
        return player_info
