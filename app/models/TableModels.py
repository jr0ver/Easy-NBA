"""
Contains the SQL relational tables for Player, RegularSeason,
PostSeason and PlayerInfo objects.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# SQLite TABLES
class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    reg_stats = db.relationship("RegularSeason", backref="player", lazy=True)
    post_stats = db.relationship("PostSeason", backref="player", lazy=True)
    player_info = db.relationship("PlayerInfo", uselist=False, lazy=True)

class RegularSeason(db.Model):
    __tablename__ = "regular_season"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    season = db.Column(db.String(10), nullable=False)
    team = db.Column(db.String(5), nullable=True)
    pos = db.Column(db.String(5), nullable=True)
    games = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)
    steals = db.Column(db.Float, nullable=True)
    blocks = db.Column(db.Float, nullable=True)

    __table_args__ = (
        db.Index('ix_regular_season_player_season', 'player_id', 'season'),
    )

class PostSeason(db.Model):
    __tablename__ = "post_season"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    season = db.Column(db.String(10), nullable=False)
    team = db.Column(db.String(5), nullable=True)
    pos = db.Column(db.String(5), nullable=True)
    games = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)
    steals = db.Column(db.Float, nullable=True)
    blocks = db.Column(db.Float, nullable=True)

    __table_args__ = (
        db.Index('ix_post_season_player_season', 'player_id', 'season'),
    )

class PlayerInfo(db.Model):
    __tablename__ = "player_info"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    link = db.Column(db.String(255), nullable=True)
    positions = db.Column(db.String(255), nullable=True)
    teams = db.Column(db.String(255), nullable=True)
    awards = db.Column(db.String(255), nullable=True)
    case_name = db.Column(db.String(100), nullable=True)

    # removed back reference since it's not needed
