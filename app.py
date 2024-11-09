from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import matplotlib

from data_cleaning import front_end_clean
from handler import handle_player_data
from models import db
from similarity import get_closest_player

# Basic configurations
matplotlib.use("Agg")  # Use Agg backend (non-interactive)
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def home():
    reg = None
    playoffs = None
    player_info = None
    user_input=None
    closest_player = None

    if request.method == "POST":
        user_input = request.form["player"].title()

        received_data = handle_player_data(user_input)

        if received_data:
            player_obj, reg, playoffs, player_info = received_data
            reg, playoffs = front_end_clean(reg), front_end_clean(playoffs)
            
            if player_obj:
                closest_player = get_closest_player(player_obj.id)

    return render_template(
        "index.html",
        reg=reg.to_html(classes="data") if reg is not None else None,
        playoffs=playoffs.to_html(classes="data") if playoffs is not None else None,
        player_info=player_info,
        closest_player = closest_player
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
