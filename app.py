from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import matplotlib

from data_cleaning import front_end_clean
from database import add_player, convert_reg_to_df, convert_post_to_df, get_player_info, get_player_object, get_player_tables
from models import db

from BasketballReference import BasketballReference
from data_retrieval import PlayerInfo
from similarity import get_closest_player

# Basic configurations
matplotlib.use("Agg")  # Use Agg backend (non-interactive)
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def home():
    player = None
    reg = None
    playoffs = None
    player_info = None
    user_input=None
    closest_player = None

    if request.method == "POST":
        user_input = request.form["player"].title()
        player_lower = user_input.lower()

        player_obj = get_player_object(player_lower) 

        # player already in DB, READ
        if player_obj:
            print("Player is already in the database")

            reg_query, playoffs_query = get_player_tables(player_obj)
            reg, playoffs = convert_reg_to_df(reg_query), convert_post_to_df(playoffs_query)
            reg, playoffs = front_end_clean(reg), front_end_clean(playoffs)
            player_info = get_player_info(player_lower)

        # player not in DB, WRITE
        else:
            print("Player is NEW")
            try:
                # since player is not in DB, need to scrape data
                player_cleaned = user_input.replace("'", "").lower().split()
                player_cleaned = player_cleaned[0] + "_" + player_cleaned[1]
                
                player_raw = BasketballReference(user_input)
                player = PlayerInfo(player_raw)
                
                reg, playoffs = player.reg, player.post
                reg, playoffs = front_end_clean(reg), front_end_clean(playoffs)

                player_info = player.get_player_info()

                add_player(player_lower, reg, playoffs, player_info)
                player_obj = get_player_object(player_lower)

            except Exception as e:
                print("Sorry, the player couldn't be found", e)
        
        # GET CLOSEST PLAYER - MIGRATE LATER
        if player_obj:
                closest_player = get_closest_player(player_obj.id)

    return render_template(
        "index.html",
        reg=reg.to_html(classes="data") if reg is not None else None,
        playoffs=playoffs.to_html(classes="data") if playoffs is not None else None,
        player=user_input,
        player_info=player_info,
        closest_player = closest_player
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
