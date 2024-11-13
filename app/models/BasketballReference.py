"""
Contains the BasketBallReference object that instantiates fields
through web requests and data scraping.
"""

from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

class BasketballReference:
    def __init__(self, name: str):
        self.name = name
        self.url, self.soup = self.get_br_page(name)  # get URL and soup together

    def set_name(self, str):
        self.name = str

    def get_br_page(self, player: str) -> tuple:
        """Returns the link to the basketball reference of the player and a BeautifulSoup object."""
        if not player:
            return "", None
        
        BR_TEMPLATE = "https://www.basketball-reference.com"
        BR_SUBHEADING = "/players/"
        
        last_initial = player.split()

        if len(last_initial) > 1:
            last_initial = last_initial[1][0].lower()
        else:
            return "", None

        new_url = BR_TEMPLATE + BR_SUBHEADING + last_initial + "/"
        try:
            # first request (1/2)
            response = requests.get(new_url)

            soup = BeautifulSoup(response.content, "html.parser")

            # for edge cases like 'DeMar DeRozan'
            regex = re.compile(player, re.IGNORECASE)
            player_link = soup.find("a", string=regex)

            self.set_name(player_link.get_text())
            # print(player_link.get_text())

            if player_link:
                player_url = BR_TEMPLATE + player_link["href"] + "/"
                    
                # fetch and parse the player's page (2/2 requests)
                player_response = requests.get(player_url)
                player_soup = BeautifulSoup(player_response.content, 'html.parser')
                
                return player_url, player_soup

            print("Player not found")
            return "", None
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return "", None

    def get_regular_season_stats(self) -> pd.DataFrame:
        """retrieves the regular season statistics of the player"""
        table_html = self.soup.find('table', {'id': 'per_game_stats'})
        if table_html:
            return pd.read_html(StringIO(str(table_html)))[0]
        else:
            print("Regular season stats table not found.")
            return pd.DataFrame()

    def get_playoff_stats(self) -> pd.DataFrame:
        """retrieves the playoff statistics of the player"""
        table_html = self.soup.find('table', {'id': 'per_game_stats_post'})
        if table_html:
            return pd.read_html(StringIO(str(table_html)))[0]
        else:
            print("Playoff stats table not found.")
            return pd.DataFrame()
        
    def get_player_div(self) -> BeautifulSoup:
        """fetches and returns the player div object for the player's page"""
        if self.soup:
            info_div = self.soup.find('div', id='info')
            return info_div
        return None
    
    def get_br_img(self) -> str:
        """fetches and returns the player's image source"""
        temp_img = self.get_player_div().find("img") if self.get_player_div() else None
        if temp_img:
            return temp_img["src"]
        return ""