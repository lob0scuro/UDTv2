from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from instance.config import DB, DB_PASSWORD, DB_SERVER, DB_USERNAME, SECRET_KEY

db = SQLAlchemy()

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB}"
	app.config['SECRET_KEY'] = SECRET_KEY
	with app.app_context():
		db.init_app(app)

	
	from . import auth
	app.register_blueprint(auth.authBP)
	from . import main
	app.register_blueprint(main.mainBP)
	app.add_url_rule('/', endpoint='index')


	return app

app = create_app()