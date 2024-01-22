from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from main import main_bp
import os


from models import db

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    app.register_blueprint(main_bp)
    CORS(app, resources={r"*": {"origins": "*"}})

    return app


app = create_app()


