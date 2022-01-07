from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create new database table if one doesn't exist
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    room = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(500))
    created_at = db.Column(db.DateTime)