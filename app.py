from dotenv import load_dotenv
import os
from app import create_app
from app.utils.app_logger import setup_logger
from app.utils.app_metrics import setup_metrics


load_dotenv()
config_name = os.getenv('FLASK_CONFIG', 'development')

app = create_app(config_name)

# Setup logger and metrics
logger = setup_logger(__name__)
metrics = setup_metrics(app)

if __name__ == '__main__':
    app.run()
