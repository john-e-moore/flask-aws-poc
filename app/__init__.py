import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from .utils.scheduler import schedule_csv_download
from .utils.s3_utils import download_csv_from_s3

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Download projections
    app.config['LAST_UPDATED'] = download_csv_from_s3(
        os.getenv('FLASK_S3_BUCKET'),
        os.getenv('FLASK_S3_KEY'),
        Config.PROJECTIONS_DOWNLOAD_LOCAL_KEY
    )
    # Schedule future projections downloads
    schedule_csv_download()

    return app
