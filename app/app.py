from flask import Flask, jsonify, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib

from app.database.db_operations import delete_player_from_id, get_player_name

from .data_cleaning import front_end_clean
from .handler import handle_player_data
from .models.TableModels import db
from .similarity import get_closest_player

# Basic configurations
matplotlib.use("Agg")  # Use Agg backend (non-interactive)
app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def home():
    reg = playoffs = player_info = user_input = player_obj = closest_player = None

    reset_name = request.args.get('reset')
    
    if request.method == "POST" or reset_name:
        if reset_name:
            user_input = reset_name
        else:
            user_input = request.form.get("player", "").title()

        received_data = handle_player_data(user_input)

        if received_data:
            player_obj, reg, playoffs, player_info = received_data
            reg, playoffs = front_end_clean(reg), front_end_clean(playoffs)
            
            if player_obj:
                closest_player = get_closest_player(player_obj.id)
    
    return render_template(
        "index.html",
        player_id=player_obj.id if player_obj is not None else None,
        reg=reg.to_html(classes="data") if reg is not None else None,
        playoffs=playoffs.to_html(classes="data") if playoffs is not None else None,
        player_info=player_info,
        closest_player=closest_player,
    )

@app.route('/delete_player', methods=['POST'])
def delete_player():
    data = request.get_json()  # extracts JSON data from the JS
    player_id = data.get('player_id')  # retrieves player_id from the JSON data
    
    p_name = get_player_name(player_id)

    # does deletion
    if delete_player_from_id(player_id):
        return redirect(url_for('home', reset=p_name,))

    else:
        return jsonify({'error': 'Player could not be found or deleted'})