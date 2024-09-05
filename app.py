from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib
from bball_ref import *
from land_of_bball import *
from data_retrieval import *

# Basic configurations
matplotlib.use("Agg")  # Use Agg backend (non-interactive)
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


# SQL TABLES
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
        player = request.form["player"]
        player = player.title()
        try:
            player_cleaned = player.replace("'", "").lower().split()
            player_cleaned = player_cleaned[0] + "_" + player_cleaned[1]

            url = (
                "https://www.landofbasketball.com/nba_players/"
                + player_cleaned
                + ".htm"
            )
            data = pd.read_html(url)

            # obtain the regular season, playoffs, and additional information
            [reg, playoffs] = get_tables(data)
            player_info = get_player_info(player, reg)

        except Exception as e:
            print("Sorry, the player couldn't be found", e)
    return render_template(
        "index.html",
        reg=reg.to_html(classes="data") if reg is not None else None,
        playoffs=playoffs.to_html(classes="data") if playoffs is not None else None,
        player=player,
        player_info=player_info,
    )


if __name__ == "__main__":
    app.run(debug=True)
