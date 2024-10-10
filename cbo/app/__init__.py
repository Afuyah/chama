from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Load User Loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import User model
        return User.query.get(int(user_id))

    # Register blueprints for different roles
    from .org.chairman import chairman_bp
    from .org.secretary import secretary_bp
    from .org.treasurer import treasurer_bp
    from .org.organizing_secretary import organizing_secretary_bp
    from .org.member_rep import member_representative_bp
    from .org.patron import patron_bp

    app.register_blueprint(chairman_bp, url_prefix='/chairman')
    app.register_blueprint(secretary_bp, url_prefix='/secretary')
    app.register_blueprint(treasurer_bp, url_prefix='/treasurer')
    app.register_blueprint(organizing_secretary_bp, url_prefix='/organizing_secretary')
    app.register_blueprint(member_representative_bp, url_prefix='/member_representative')
    app.register_blueprint(patron_bp, url_prefix='/patron')

    return app
