from pathlib import Path

from flask import Flask
from alembic.config import Config as AlembicConfig
from alembic import command

from config import config
from files.routers import router

app = Flask(__name__)
app.register_blueprint(router)

Path(config.storage_path).mkdir(parents=True, exist_ok=True)

command.upgrade(AlembicConfig("../alembic.ini"), "head")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
