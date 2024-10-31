from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib

from BasketballReference import BasketballReference
from data_retrieval import PlayerInfo

# Basic configurations
matplotlib.use("Agg")  # Use Agg backend (non-interactive)
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


# SQLite TABLES
class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    positions = db.Column(db.String(200), nullable=False)
    teams = db.Column(db.String(1000), nullable=False)
    championships = db.Column(db.Integer, nullable=False)
    all_stars = db.Column(db.Integer, nullable=False)
    all_nbas = db.Column(db.Integer, nullable=False)
    seasons_played = db.Column(db.Integer, nullable=False)

    reg_season = db.relationship("RegularSeason", backref="player")
    playoffs = db.relationship("Playoffs", backref="player")

    def __repr__(self):
        return f"{self.name.title()} with ID:{self.id}"


class RegularSeason(db.Model):
    __tablename__ = "regular_season"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    season = db.Column(db.String(200), nullable=False)
    team = db.Column(db.String(200), nullable=False)
    games = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)
    steals = db.Column(db.Float, nullable=False)
    blocks = db.Column(db.Float, nullable=False)


class Playoffs(db.Model):
    __tablename__ = "playoffs"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    season = db.Column(db.String(200), nullable=False)
    team = db.Column(db.String(200), nullable=False)
    games = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)
    steals = db.Column(db.Float, nullable=False)
    blocks = db.Column(db.Float, nullable=False)


@app.route("/", methods=["GET", "POST"])
def home():
    db.create_all()
    db.session.commit()
    player = None
    reg = None
    playoffs = None
    player_info = None

    if request.method == "POST":
        player_input = request.form["player"].title()
        try:
            player_cleaned = player_input.replace("'", "").lower().split()
            player_cleaned = player_cleaned[0] + "_" + player_cleaned[1]

            # url = (
            #     "https://www.landofbasketball.com/nba_players/"
            #     + player_cleaned
            #     + ".htm"
            # )
            # data = pd.read_html(url)

            # # obtain the regular season, playoffs, and additional information
            # [reg, playoffs] = get_tables(data)

            # player = BasketballReference(player_input)
            # reg = clean_table(player.get_regular_season_stats())
            # playoffs = clean_table(player.get_playoff_stats())
            
            player_raw = BasketballReference(player_input)
            player = PlayerInfo(player_raw)
            reg = player.reg
            playoffs = player.post
            player_info = player.get_player_info()
            # print(reg)
        except Exception as e:
            print("Sorry, the player couldn't be found", e)
    
    awards = [
        {"name": "MVP", "year": 2021},
        {"name": "ROY", "year": 2022},
        {"name": "DPOY", "year": 2020}
    ]

    return render_template(
        "index.html",
        reg=reg.to_html(classes="data") if reg is not None else None,
        playoffs=playoffs.to_html(classes="data") if playoffs is not None else None,
        player=player_input,
        player_info=player_info,
        awards=awards
    )


if __name__ == "__main__":
    app.run(debug=True)
