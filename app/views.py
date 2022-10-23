from flask import Blueprint, render_template, current_app, request, flash
from sqlalchemy.orm import session
from models import Food, db

mp = Blueprint('meal_planner', __name__, template_folder='templates', static_folder='static')


@mp.route('/')
def hello_world():
    return render_template('food.html', foods=Food.query.all())


@mp.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
        print(request.form)
        print(request.form.getlist('food_type'))
        # mutate data preparing it for DB insertion
        food_type = 0
        f_type = {
            'breakfast': 1,
            'lunch': 2,
            'dinner': 4,
        }
        for _ in request.form.getlist('food_type'):
            food_type += f_type[_]

        new_food = Food(
            source=request.form.get('source').replace('grubhub', 'doordash'),
            vendor=request.form.get('vendor'),
            name=request.form.get('name'),
            details=request.form.get('details'),
            calories=int(request.form.get('calories')),
            notes=request.form.get('notes'),
            food_type=food_type,
            cost=int(request.form.get('cost')),
        )

        try:
            db.session.add(new_food)
            db.session.commit()
            return 'Added Food'
        except Exception as e:
            return f'Failed to add food: {e}'
    else:
        return 'BAD'
