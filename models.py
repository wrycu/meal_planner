from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    source = db.Column(db.Enum('doordash', 'hello_fresh', 'self'), nullable=False)
    vendor = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text)
    calories = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    food_type = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    added = db.Column(db.Date, nullable=False, server_default='CURDATE')

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'source': self.source,
            'vendor': self.vendor,
            'name': self.name,
            'details': self.details,
            'calories': self.calories,
            'notes': self.notes,
            'food_type': self.food_type,
            'cost': self.cost,
            'added': str(self.added),
        })


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    calories_s = db.Column(db.Integer)
    last_consumed = db.Column(db.Date, nullable=False, server_default="CURDATE")
    consume_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'notes': self.notes,
            'calories_s': self.calories_s,
            'last_consumed': str(self.last_consumed),
        })


class MealMap(db.Model):
    meal_id = db.Column(db.Integer, db.ForeignKey(Meal.id), primary_key=True, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey(Food.id), primary_key=True, nullable=False)

    def __repr__(self):
        return json.dumps({
            'meal_id': self.meal_id,
            'food_id': self.food_id,
        })
