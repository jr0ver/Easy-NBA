import pandas as pd
from bs4 import BeautifulSoup
import matplotlib
from bball_ref import *
from land_of_bball import *

def convert_type(df: pd.DataFrame) -> pd.DataFrame:
    numerical_columns = ["Games", "Points", "Rebounds", "Assists", "Steals", "Blocks"]
    for col in numerical_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def get_tables(data: pd.Series) -> tuple:
    reg = data[len(data) - 2]
    playoffs = data[len(data) - 1]
    column_names = [
        "Season",
        "Team",
        "Games",
        "Points",
        "Rebounds",
        "Assists",
        "Steals",
        "Blocks",
        "NaN",
    ]

    tables = {"reg": reg, "playoffs": playoffs}

    # loop over the two tables to clean the raw data
    for name, df in tables.items():
        df.columns = column_names
        df = df.drop(0).drop("NaN", axis=1)
        df = df.reset_index(drop=True)
        df.index += 1
        tables[name] = df

    reg = convert_type(tables["reg"])
    playoffs = convert_type(tables["playoffs"])

    # career average value is NaN, this changes to season

    if pd.isna(reg["Season"].iloc[-1]):
        reg.loc[reg.index[-1], "Season"] = "Career"

    if pd.isna(playoffs["Season"].iloc[-1]):
        playoffs.loc[playoffs.index[-1], "Season"] = "Career"

    return reg, playoffs


def get_player_info(player: str, reg: pd.DataFrame) -> dict[str]:
    """Given a player, the function calls functions from the modules
    land_of_bball.py and bbal_ref.py to sequentially obtain and produce
    a dictionary of various player information
    """
    result = get_br_page(player)
    soup = result[0]  # entire basketball reference page
    player_name = result[1]  # player name
    img_link = get_br_img(soup)
    position = get_position(get_br_info(soup))

    teams = find_top_teams(reg)
    player_info = {
        "player_name": player_name,
        "img_link": img_link,
        "position": position,
        "teams": teams,
    }
    # show_graph(reg)
    return player_info
