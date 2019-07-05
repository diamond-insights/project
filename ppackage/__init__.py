from flask import Flask

from flask_mail import Mail, Message

from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

app = Flask(__name__, static_folder="static", instance_relative_config=True)

csrf = CSRFProtect(app)

mail = Mail(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

app.config.from_pyfile('config.py')



from ppackage import views, api