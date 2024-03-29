from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
# from instance.conf import config
with open("/etc/config.json", encoding="utf-8") as config_file:
   config = json.load(config_file)
db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = config["SQLALCHEMY_DATABASE_URI"]
    app.config['SECRET_KEY'] = config["SECRET_KEY"]
    with app.app_context():
        db.init_app(app)

    migrate.init_app(app, db)

    from . import auth
    app.register_blueprint(auth.authBP)
    from . import main
    app.register_blueprint(main.mainBP)
    app.add_url_rule('/', endpoint='index')
    return app


app = create_app()
