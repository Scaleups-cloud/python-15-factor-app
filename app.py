from dotenv import load_dotenv
import os
from app import create_app

load_dotenv()
flask_env = os.getenv('FLASK_ENV', 'development')

app = create_app(flask_env)

if __name__ == '__main__':
    app.run()
