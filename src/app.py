from pathlib import Path
from files import routers

from flask import Flask

from src.config import Config

app = Flask(__name__)
app.register_blueprint(routers.router)

Path(Config.STORAGE_PATH).mkdir(parents=True, exist_ok=True) if Config.DOCKER == 'False' else None


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
