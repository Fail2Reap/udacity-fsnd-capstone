from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app):
    """Binds a database to a Flask application.

    Args:
        app (Flask): The application to bind the database to.
    """
    db.app = app
    db.init_app(app)

    # Ensure that the database binding knows of our models
    import backend.database.models


def reset_db():
    """Drops all tables and recreates them."""
    db.drop_all()
    db.create_all()
