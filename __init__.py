from flask import Flask
# from database import db, History

def create_app():
    # Construct the core application 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'youwontknow'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'

    with app.app_context():
        from database import db, History
        from views import views

        app.register_blueprint(views, url_prefix="")
        db.init_app(app)

    return app