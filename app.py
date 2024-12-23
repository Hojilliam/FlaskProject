from flask import Flask, request, jsonify
from extensions import db
from extensions import client
from models import User, Spending
from sqlalchemy import inspect, and_

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_vouchers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create tables at startup
with app.app_context():
    db.create_all()


# @app.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     new_user = User(**data)
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# @app.route("/users/<int:user_id>", methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.get_or_404(user_id)
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': 'User deleted!'})

# Unfinished - returns single value instead of list of all values
@app.route("/total_spent/<int:user_id>", methods=['GET'])
def get_total_spent(user_id):
    user = User.query.get_or_404(user_id)

    spending = Spending.query.filter_by(user_id=user_id).all()
    total_spent = 0
    for value in spending:
        total_spent += value.money_spent

    data = {
        'user_id': user.user_id,
        'money_spent': total_spent
    }

    return jsonify(data)

@app.route('/average_spending_by_age', methods=['GET'])
def get_avg_by_age():
    users18_24 = User.query.filter(and_(User.age >= 18, User.age <= 24)).all()
    users18_24_list = []
    for user in users18_24:
        users18_24_list.append(user.user_id)

    users18_24_spending = 0
    counter = 0
    for user_id in users18_24_list:
        iterator = Spending.query.filter_by(user_id=user_id).all()
        for value in iterator:
            users18_24_spending += value.money_spent
            counter += 1
    users18_24_spending /= counter
# --------------------------------------
    users25_30 = User.query.filter(and_(User.age >= 25, User.age <= 30)).all()
    users25_30_list = []
    for user in users25_30:
        users25_30_list.append(user.user_id)

    users25_30_spending = 0
    counter = 0
    for user_id in users25_30_list:
        iterator = Spending.query.filter_by(user_id=user_id).all()
        for value in iterator:
            users25_30_spending += value.money_spent
            counter += 1
    users25_30_spending /= counter
# --------------------------------------

    data = {
        'age 18 - 24': users18_24_spending,
        'age 25 - 30': users25_30_spending
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
