from flask import Flask
import toml
from models import db
from app.views import mp


app = Flask(__name__, static_folder='app/static')
app.config.from_object('config')
app.config.from_file('config.ini', load=toml.load, silent=False)

app.register_blueprint(mp)

db.init_app(app)
app.run(host='127.0.0.1')


#app.config['DB'] = db
