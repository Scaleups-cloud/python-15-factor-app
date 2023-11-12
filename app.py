from dotenv import load_dotenv
import os
from app import create_app
from app.utils.app_logger import setup_logger
from app.utils.app_metrics import setup_metrics


load_dotenv()
flask_env = os.getenv('FLASK_ENV', 'development')

app = create_app(flask_env)

# Setup logger and metrics
logger = setup_logger(__name__)
metrics = setup_metrics(app)

if __name__ == '__main__':
    app.run()
