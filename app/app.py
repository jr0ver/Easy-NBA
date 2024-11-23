"""
Module responsible for initializing Flask app and b asic configs. This file
also contains major app_routes such as the home and delete app route.
"""

from flask import Flask, jsonify, redirect, request, render_template, url_for
from flask_migrate import Migrate

from .handler import handle_closest_player, handle_deletion_status, handle_player_data
from .models.TableModels import db

app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/", methods=["GET", "POST"])
def home():
    reg = playoffs = player_info = user_input = player_obj = closest_player = None
    reset_name = request.args.get('reset') # if app route is redirected by home
    
    if request.method == "POST" or reset_name:
        if reset_name:
            user_input = reset_name
        else:
            user_input = request.form.get("player", "").title()

        received_data = handle_player_data(user_input)

        if received_data:
            player_obj, reg, playoffs, player_info = received_data
            
            if player_obj:
                closest_player = handle_closest_player(player_obj.id)
                # closest_player = "Oops! There has been an error calculating the closest player."

    
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
    
    p_name, deleted = handle_deletion_status(player_id)

    # does deletion
    if deleted:
        return redirect(url_for('home', reset=p_name,))
    else:
        return jsonify({'error': 'Player could not be found or deleted'})