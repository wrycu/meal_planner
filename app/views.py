from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for
from sqlalchemy.orm import session
from models import Food, Meal, MealMap, db

mp = Blueprint('meal_planner', __name__, template_folder='templates', static_folder='static')


@mp.route('/')
def hello_world():
    return redirect(url_for('meal_planner.food'))


@mp.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
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
        return render_template('food.html', foods=Food.query.all())


@mp.route('/meal', methods=['GET', 'POST'])
def meal():
    if request.method == 'POST':
        # mutate data preparing it for DB insertion
        meal_type = 0
        f_type = {
            'breakfast': 1,
            'lunch': 2,
            'dinner': 4,
        }
        for _ in request.form.getlist('type'):
            meal_type += f_type[_]

        foods = request.form.getlist('food')

        new_meal = Meal(
            type=meal_type,
            name=request.form.get('name'),
            notes=request.form.get('notes'),
            calories_s=0,
            consume_count=0,
        )
        db.session.add(new_meal)
        db.session.commit()
        db.session.refresh(new_meal)
        for food in foods:
            db.session.add(MealMap(
                meal_id=new_meal.id,
                food_id=int(food),
            ))
        db.session.commit()
        print(request.form)
        return 'GOOD'
    else:
        meals_temp = Meal.query.all()
        foods = Food.query.all()
        meals = []
        for meal in meals_temp:
            tmp = {
                'id': meal.id,
                'type': meal.type,
                'name': meal.name,
                'notes': meal.notes,
                'calories_s': meal.calories_s,
                'calories_c': 0,
                'cost_c': 0,
                'last_consumed': meal.last_consumed,
                'consume_count': meal.consume_count,
                'foods': [],
            }

            for item in MealMap.query.filter(MealMap.meal_id == meal.id).all():
                for food in Food.query.filter(Food.id == item.food_id).all():
                    tmp['foods'].append({
                        'id': food.id,
                        'source': food.source,
                        'vendor': food.vendor,
                        'name': food.name,
                        'details': food.details,
                        'calories': food.calories,
                        'notes': food.notes,
                        'cost': food.cost,
                        'added': food.added,
                    })
                    tmp['calories_c'] += food.calories
                    tmp['cost_c'] += food.cost
            meals.append(tmp)
        return render_template('meal.html', meals=meals, foods=foods)


@mp.route('/logger', methods=['GET', 'POST'])
def logger():
    return render_template('logger.html')


@mp.route('/planner', methods=['GET', 'POST'])
def planner():
    return render_template('planner.html')
