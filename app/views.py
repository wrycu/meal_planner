from flask import Blueprint, render_template, current_app
from sqlalchemy.orm import session
from models import Food

mp = Blueprint('meal_planner', __name__, template_folder='templates')


@mp.route('/')
def hello_world():
    return render_template('base.html', foods=Food.query.all())
