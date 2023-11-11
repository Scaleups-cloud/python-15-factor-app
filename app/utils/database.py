from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy ORM instance
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the given Flask app context.
    """
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

def reset_database():
    """
    Drop all tables and recreate them.
    Use with caution, as this will erase all data!
    """
    with db.engine.connect() as conn:
        conn.execute('DROP SCHEMA public CASCADE;')
        conn.execute('CREATE SCHEMA public;')

    db.create_all()

def check_database_connection():
    try:
        db.engine.execute('SELECT 1')
        return True
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return False
