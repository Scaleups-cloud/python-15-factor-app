from dotenv import load_dotenv
from app import create_app
import os

load_dotenv()
flask_env = os.getenv('FLASK_ENV', 'development')  # Default to 'development' if not set

app = create_app(flask_env)  # or 'production', 'testing', etc.

if __name__ == '__main__':
    app.run()
