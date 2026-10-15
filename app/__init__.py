
import os, signal, datetime
from flask import Flask, redirect, url_for, session, url_for, flash
from flask_login import LoginManager, current_user, logout_user

# Local Imports
from config import Config
from app.extensions import db, logger, globals
from app.functions import get_data


def create_app(config_class=Config):
    app = Flask(__name__, static_folder=f"{globals.basedir}/app/static/",template_folder=f"{globals.basedir}/app/templates/")
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False

    from app.models import Anonymous, User
    login_manager = LoginManager()
    login_manager.login_view = "main.login"
    login_manager.anonymous_user = Anonymous
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.main.main import main as main_blueprint
    
    from app.auth.auth import auth as auth_blueprint

    db.init_app(app)
    with app.app_context():
        db.create_all()

        def signal_handler(sig,frame):
            logger.info(f"Signal Received -- Shutting down site")
            os._exit(0)

        signal.signal(signal.SIGTSTP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        @app.errorhandler(404)
        def page_not_found(e):
            if current_user.is_authenticated:
                return redirect(url_for("auth.accounts"))
            return redirect(url_for("main.login"))

        @main_blueprint.before_request
        @auth_blueprint.before_request        
        def check_session():
            if current_user.is_authenticated:
                cur_time = datetime.datetime.now(datetime.timezone.utc)
                time_diff = cur_time - session['last_activity']
                if time_diff > globals.auto_logout:
                    logout_user()
                    session.pop('last_acitivity', None)
                    flash("Your session has timed out. Please log in again.")
                    return redirect(url_for('main.login'))
                else:
                    session['last_activity'] = datetime.datetime.now(datetime.timezone.utc)


    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    
    app.add_url_rule("/api", view_func=get_data, endpoint='/api')

    return app
