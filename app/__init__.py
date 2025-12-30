import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        # Handle error if instance path cannot be created, though exist_ok=True should prevent most issues
        pass

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db') # Default if not set
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    # Import models here to ensure they are registered with SQLAlchemy
    # By importing them, SQLAlchemy becomes aware of them.
    from app.models import User, Property

    @app.route('/health') # Adding a simple health check endpoint
    def health():
        return 'OK', 200

    return app
