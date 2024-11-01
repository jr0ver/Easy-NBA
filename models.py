from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# SQLite TABLES
class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

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

Player.reg_stats = db.relationship("RegularSeason", backref="player", lazy=True)
Player.post_stats = db.relationship("PostSeason", backref="player", lazy=True)
