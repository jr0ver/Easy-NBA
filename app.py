from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import matplotlib

from database import add_player, convert_reg_to_df, convert_post_to_df, get_player_data, get_player_info
from models import db

from BasketballReference import BasketballReference
from data_retrieval import PlayerInfo

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
    player_input=None

    if request.method == "POST":
        player_input = request.form["player"].title()
        player_query = player_input.lower()

        reg_query, playoffs_query = get_player_data(player_query)
        # player already in DB, READ
        if reg_query:
            print("Player is already in the database")
            # convert SQL data to DF
            reg, playoffs = convert_reg_to_df(reg_query), convert_post_to_df(playoffs_query)
            player_info = get_player_info(player_query)
        
        # player not in DB, WRITE
        else:
            print("Player is NEW")
            try:
                # since player is not in DB, need to scrape data
                player_cleaned = player_input.replace("'", "").lower().split()
                player_cleaned = player_cleaned[0] + "_" + player_cleaned[1]
                
                player_raw = BasketballReference(player_input)
                player = PlayerInfo(player_raw)
                reg = player.reg
                playoffs = player.post
                player_info = player.get_player_info()

                add_player(player_query, reg, playoffs, player_info)

            except Exception as e:
                print("Sorry, the player couldn't be found", e)
    
    return render_template(
        "index.html",
        reg=reg.to_html(classes="data") if reg is not None else None,
        playoffs=playoffs.to_html(classes="data") if playoffs is not None else None,
        player=player_input,
        player_info=player_info,
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
