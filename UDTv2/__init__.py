from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from instance.config import *

db = SQLAlchemy()

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB}"
	with app.app_context():
		db.init_app(app)

	
	from . import auth
	app.register_blueprint(auth.authBP)

	@app.route("/")	
	def index():
		return render_template('index.html')

	return app

