from backend.sherlockgpt.database import db

class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    style = db.Column(db.String(100), nullable=False)
    setting = db.Column(db.Text, nullable=False)
    crime = db.Column(db.Text, nullable=False)
    newspaper_headline = db.Column(db.Text, nullable=False)
    newspaper_text = db.Column(db.Text, nullable=False)
    intro = db.Column(db.Text, nullable=False)
    secret_truth = db.Column(db.Text, nullable=False)
    victim = db.Column(db.Text, nullable=False)
    location_info = db.Column(db.Text, nullable=False)
    plot_twists = db.Column(db.Text, nullable=False)
    crime_scene_description = db.Column(db.Text, nullable=False)

    characters = db.relationship('Character', backref='scenario', lazy=True)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    appearance = db.Column(db.Text, nullable=False)
    personality = db.Column(db.Text, nullable=False)
    relationships = db.Column(db.Text, nullable=False)
    involvement = db.Column(db.Text, nullable=False)
    is_dead = db.Column(db.Boolean, nullable=False)
    is_criminal = db.Column(db.Boolean, nullable=False)
    is_victim = db.Column(db.Boolean, nullable=False)
    knowledge = db.Column(db.Text, nullable=False)
    feelings = db.Column(db.Text, nullable=False)
    alibi = db.Column(db.Text, nullable=False)
    activities = db.Column(db.Text, nullable=False)
    topics = db.Column(db.Text, nullable=False)
    motives = db.Column(db.Text, nullable=False)
    relevant_info = db.Column(db.Text, nullable=False)