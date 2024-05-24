from pathlib import Path

from flask import Flask
from alembic.config import Config as AlembicConfig
from alembic import command

from config import Config
from files.routers import router

app = Flask(__name__)
app.register_blueprint(router)

Path(Config.STORAGE_PATH).mkdir(parents=True, exist_ok=True)

command.upgrade(AlembicConfig("/app/alembic.ini"), "head")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
