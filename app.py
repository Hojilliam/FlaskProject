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


def get_avg(user_list):
    users25_30_spending = 0
    counter = 0
    for user_id in user_list:
        iterator = Spending.query.filter_by(user_id=user_id).all()
        for value in iterator:
            users25_30_spending += value.money_spent
            counter += 1
    return users25_30_spending / counter

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Unfinished - returns single value instead of list of all values
@app.route("/total_spent/<int:user_id>", methods=['GET'])
def get_total_spent(user_id):

    spending = Spending.query.filter_by(user_id=user_id).all()

    print(spending)

    for spent in spending:
        print(spent)

    total_spent = 0
    for value in spending:
        total_spent += value.money_spent

    data = {
        'user_id': user_id,
        'total_spent': total_spent
    }

    return jsonify(data)

# To be modified/shortened again and checked for accuracy
@app.route('/average_spending_by_age', methods=['GET'])
def get_avg_by_age():
    users18_24 = User.query.filter(and_(User.age >= 18, User.age <= 24)).all()
    users18_24_list = []
    for user in users18_24:
        users18_24_list.append(user.user_id)

    age18_24 = get_avg(users18_24_list)
# --------------------------------------
    users25_30 = User.query.filter(and_(User.age >= 25, User.age <= 30)).all()
    users25_30_list = []
    for user in users25_30:
        users25_30_list.append(user.user_id)

    age25_30 = get_avg(users25_30_list)
# --------------------------------------
    users31_36 = User.query.filter(and_(User.age >= 31, User.age <= 36)).all()
    users31_36_list = []
    for user in users31_36:
        users31_36_list.append(user.user_id)

    age31_36 = get_avg(users31_36_list)
# --------------------------------------
    users37_47 = User.query.filter(and_(User.age >= 37, User.age <= 47)).all()
    users37_47_list = []
    for user in users37_47:
        users37_47_list.append(user.user_id)

    age37_47 = get_avg(users37_47_list)
# --------------------------------------
    users47 = User.query.filter(User.age > 47).all()
    users47_list = []
    for user in users47:
        users47_list.append(user.user_id)

    age47 = get_avg(users47_list)


    data = {
        'age 18 - 24': round(age18_24, 3),
        'age 25 - 30': round(age25_30, 3),
        'age 31 - 36': round(age31_36, 3),
        'age 37 - 47': round(age37_47, 3),
        'age 47+': round(age47, 3)
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
